from exports import Exports
from imports import add_imports_to_linker, Imports
from typing import Tuple, List
import exports as e
import imports as i
import sys
import wasmtime

class MyImports:
    def list_roundtrip(self, a: bytes) -> bytes:
        return a

    def string_roundtrip(self, a: str) -> str:
        return a

def run(wasm_file: str) -> None:
    store = wasmtime.Store()
    module = wasmtime.Module.from_file(store.engine, wasm_file)
    linker = wasmtime.Linker(store.engine)
    linker.define_wasi()
    wasi = wasmtime.WasiConfig()
    wasi.inherit_stdout()
    wasi.inherit_stderr()
    store.set_wasi(wasi)

    imports = MyImports()
    add_imports_to_linker(linker, store, imports)


    # instance = linker.instantiate(store, module)
    # run = instance.exports(store)["_start"]
    # run(store)


    wasm = Exports(store, linker, module)

    allocated_bytes = wasm.allocated_bytes(store)
    wasm.test_imports(store)
    assert(wasm.string_roundtrip(store, "x") == "x")
    assert(wasm.string_roundtrip(store, "") == "")
    assert(wasm.string_roundtrip(store, "hello ⚑ world") == "hello ⚑ world")

    # Ensure that we properly called `free` everywhere in all the glue that we
    # needed to.
    assert(allocated_bytes == wasm.allocated_bytes(store))

if __name__ == '__main__':
    run(sys.argv[1])
