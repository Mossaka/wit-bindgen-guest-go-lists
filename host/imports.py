from abc import abstractmethod
import ctypes
from typing import Any, List, Tuple, cast
import wasmtime

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _store(ty: Any, mem: wasmtime.Memory, store: wasmtime.Storelike, base: int, offset: int, val: Any) -> None:
    ptr = (base & 0xffffffff) + offset
    if ptr + ctypes.sizeof(ty) > mem.data_len(store):
        raise IndexError('out-of-bounds store')
    raw_base = mem.data_ptr(store)
    c_ptr = ctypes.POINTER(ty)(
        ty.from_address(ctypes.addressof(raw_base.contents) + ptr)
    )
    c_ptr[0] = val

def _decode_utf8(mem: wasmtime.Memory, store: wasmtime.Storelike, ptr: int, len: int) -> str:
    ptr = ptr & 0xffffffff
    len = len & 0xffffffff
    if ptr + len > mem.data_len(store):
        raise IndexError('string out of bounds')
    base = mem.data_ptr(store)
    base = ctypes.POINTER(ctypes.c_ubyte)(
        ctypes.c_ubyte.from_address(ctypes.addressof(base.contents) + ptr)
    )
    return ctypes.string_at(base, len).decode('utf-8')

def _encode_utf8(val: str, realloc: wasmtime.Func, mem: wasmtime.Memory, store: wasmtime.Storelike) -> Tuple[int, int]:
    bytes = val.encode('utf8')
    ptr = realloc(store, 0, 0, 1, len(bytes))
    assert(isinstance(ptr, int))
    ptr = ptr & 0xffffffff
    if ptr + len(bytes) > mem.data_len(store):
        raise IndexError('string out of bounds')
    base = mem.data_ptr(store)
    base = ctypes.POINTER(ctypes.c_ubyte)(
        ctypes.c_ubyte.from_address(ctypes.addressof(base.contents) + ptr)
    )
    ctypes.memmove(base, bytes, len(bytes))
    return (ptr, len(bytes))

def _list_canon_lift(ptr: int, len: int, size: int, ty: Any, mem: wasmtime.Memory ,store: wasmtime.Storelike) -> Any:
    ptr = ptr & 0xffffffff
    len = len & 0xffffffff
    if ptr + len * size > mem.data_len(store):
        raise IndexError('list out of bounds')
    raw_base = mem.data_ptr(store)
    base = ctypes.POINTER(ty)(
        ty.from_address(ctypes.addressof(raw_base.contents) + ptr)
    )
    if ty == ctypes.c_uint8:
        return ctypes.string_at(base, len)
    return base[:len]

def _list_canon_lower(list: Any, ty: Any, size: int, align: int, realloc: wasmtime.Func, mem: wasmtime.Memory, store: wasmtime.Storelike) -> Tuple[int, int]:
    total_size = size * len(list)
    ptr = realloc(store, 0, 0, align, total_size)
    assert(isinstance(ptr, int))
    ptr = ptr & 0xffffffff
    if ptr + total_size > mem.data_len(store):
        raise IndexError('list realloc return of bounds')
    raw_base = mem.data_ptr(store)
    base = ctypes.POINTER(ty)(
        ty.from_address(ctypes.addressof(raw_base.contents) + ptr)
    )
    for i, val in enumerate(list):
        base[i] = val
    return (ptr, len(list))
class Imports(Protocol):
    @abstractmethod
    def list_roundtrip(self, a: bytes) -> bytes:
        raise NotImplementedError
    @abstractmethod
    def string_roundtrip(self, a: str) -> str:
        raise NotImplementedError

def add_imports_to_linker(linker: wasmtime.Linker, store: wasmtime.Store, host: Imports) -> None:
    ty = wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32(), wasmtime.ValType.i32()], [])
    def list_roundtrip(caller: wasmtime.Caller, arg0: int, arg1: int, arg2: int) -> None:
        m = caller["memory"]
        assert(isinstance(m, wasmtime.Memory))
        memory = cast(wasmtime.Memory, m)
        realloc = caller["cabi_realloc"]
        assert(isinstance(realloc, wasmtime.Func))
        ptr = arg0
        len0 = arg1
        list = cast(bytes, _list_canon_lift(ptr, len0, 1, ctypes.c_uint8, memory, caller))
        ret = host.list_roundtrip(list)
        ptr1, len2 = _list_canon_lower(ret, ctypes.c_uint8, 1, 1, realloc, memory, caller)
        _store(ctypes.c_uint32, memory, caller, arg2, 4, len2)
        _store(ctypes.c_uint32, memory, caller, arg2, 0, ptr1)
    linker.define('imports', 'list-roundtrip: func(a: list<u8>) -> list<u8>', wasmtime.Func(store, ty, list_roundtrip, access_caller = True))
    ty = wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32(), wasmtime.ValType.i32()], [])
    def string_roundtrip(caller: wasmtime.Caller, arg0: int, arg1: int, arg2: int) -> None:
        m = caller["memory"]
        assert(isinstance(m, wasmtime.Memory))
        memory = cast(wasmtime.Memory, m)
        realloc = caller["cabi_realloc"]
        assert(isinstance(realloc, wasmtime.Func))
        ptr = arg0
        len0 = arg1
        list = _decode_utf8(memory, caller, ptr, len0)
        ret = host.string_roundtrip(list)
        ptr1, len2 = _encode_utf8(ret, realloc, memory, caller)
        _store(ctypes.c_uint32, memory, caller, arg2, 4, len2)
        _store(ctypes.c_uint32, memory, caller, arg2, 0, ptr1)
    linker.define('imports', 'string-roundtrip: func(a: string) -> string', wasmtime.Func(store, ty, string_roundtrip, access_caller = True))
