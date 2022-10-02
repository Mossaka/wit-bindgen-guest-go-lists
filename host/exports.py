from abc import abstractmethod
import ctypes
from typing import Any, List, Tuple, cast
import wasmtime

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _load(ty: Any, mem: wasmtime.Memory, store: wasmtime.Storelike, base: int, offset: int) -> Any:
    ptr = (base & 0xffffffff) + offset
    if ptr + ctypes.sizeof(ty) > mem.data_len(store):
        raise IndexError('out-of-bounds store')
    raw_base = mem.data_ptr(store)
    c_ptr = ctypes.POINTER(ty)(
        ty.from_address(ctypes.addressof(raw_base.contents) + ptr)
    )
    return c_ptr[0]

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
class Exports:
    instance: wasmtime.Instance
    _allocated_bytes: wasmtime.Func
    _cabi_post_list_roundtrip: wasmtime.Func
    _cabi_post_string_roundtrip: wasmtime.Func
    _cabi_realloc: wasmtime.Func
    _list_roundtrip: wasmtime.Func
    _memory: wasmtime.Memory
    _string_roundtrip: wasmtime.Func
    _test_imports: wasmtime.Func
    def __init__(self, store: wasmtime.Store, linker: wasmtime.Linker, module: wasmtime.Module):
        self.instance = linker.instantiate(store, module)
        exports = self.instance.exports(store)
        
        allocated_bytes = exports['allocated-bytes: func() -> u32']
        assert(isinstance(allocated_bytes, wasmtime.Func))
        self._allocated_bytes = allocated_bytes
        
        cabi_post_list_roundtrip = exports['cabi_post_list-roundtrip']
        assert(isinstance(cabi_post_list_roundtrip, wasmtime.Func))
        self._cabi_post_list_roundtrip = cabi_post_list_roundtrip
        
        cabi_post_string_roundtrip = exports['cabi_post_string-roundtrip']
        assert(isinstance(cabi_post_string_roundtrip, wasmtime.Func))
        self._cabi_post_string_roundtrip = cabi_post_string_roundtrip
        
        cabi_realloc = exports['cabi_realloc']
        assert(isinstance(cabi_realloc, wasmtime.Func))
        self._cabi_realloc = cabi_realloc
        
        list_roundtrip = exports['list-roundtrip: func(a: list<u8>) -> list<u8>']
        assert(isinstance(list_roundtrip, wasmtime.Func))
        self._list_roundtrip = list_roundtrip
        
        memory = exports['memory']
        assert(isinstance(memory, wasmtime.Memory))
        self._memory = memory
        
        string_roundtrip = exports['string-roundtrip: func(a: string) -> string']
        assert(isinstance(string_roundtrip, wasmtime.Func))
        self._string_roundtrip = string_roundtrip
        
        test_imports = exports['test-imports: func() -> ()']
        assert(isinstance(test_imports, wasmtime.Func))
        self._test_imports = test_imports
    def test_imports(self, caller: wasmtime.Store) -> None:
        self._test_imports(caller)
    def allocated_bytes(self, caller: wasmtime.Store) -> int:
        ret = self._allocated_bytes(caller)
        assert(isinstance(ret, int))
        return ret & 0xffffffff
    def list_roundtrip(self, caller: wasmtime.Store, a: bytes) -> bytes:
        memory = self._memory;
        realloc = self._cabi_realloc
        ptr, len0 = _list_canon_lower(a, ctypes.c_uint8, 1, 1, realloc, memory, caller)
        ret = self._list_roundtrip(caller, ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_int32, memory, caller, ret, 0)
        load1 = _load(ctypes.c_int32, memory, caller, ret, 4)
        ptr2 = load
        len3 = load1
        list = cast(bytes, _list_canon_lift(ptr2, len3, 1, ctypes.c_uint8, memory, caller))
        self._cabi_post_list_roundtrip(caller, ret)
        return list
    def string_roundtrip(self, caller: wasmtime.Store, a: str) -> str:
        memory = self._memory;
        realloc = self._cabi_realloc
        ptr, len0 = _encode_utf8(a, realloc, memory, caller)
        ret = self._string_roundtrip(caller, ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_int32, memory, caller, ret, 0)
        load1 = _load(ctypes.c_int32, memory, caller, ret, 4)
        ptr2 = load
        len3 = load1
        list = _decode_utf8(memory, caller, ptr2, len3)
        self._cabi_post_string_roundtrip(caller, ret)
        return list
