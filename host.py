import sys
from typing import List, Tuple

import wasmtime

from host import (Descriptor, Lists, ListsImports, WasiStream, imports,
                  wasi_clocks, wasi_default_clocks, wasi_filesystem,
                  wasi_logging, wasi_poll)
from host.imports.wasi_clocks import (Datetime, Instant, MonotonicClock,
                                      WallClock)
from host.imports.wasi_filesystem import Errno, Filesize, Size
from host.imports.wasi_logging import Level
from host.imports.wasi_poll import StreamError
from host.types import Result


class MyImports(imports.Imports):
    def list_roundtrip(self, a: bytes) -> bytes:
        return a

    def string_roundtrip(self, a: str) -> str:
        return a

class Clock(wasi_clocks.WasiClocks):
    def monotonic_clock_now(self, clock: MonotonicClock) -> Instant:
        return 0
    def wall_clock_now(self, clock: WallClock) -> Datetime:
        return Datetime(0, 0)

class DefaultClock(wasi_default_clocks.WasiDefaultClocks):
    def default_monotonic_clock(self) -> MonotonicClock:
        return 0
    def default_wall_clock(self) -> WallClock:
        return 0

class Logging(wasi_logging.WasiLogging):
    def log(self, level: Level, context: str, message: str) -> None:
        print(f"{message}")

class Filesystem(wasi_filesystem.WasiFilesystem):
    def write_via_stream(self, fd: Descriptor, offset: Filesize) -> Result[WasiStream, Errno]:
        raise NotImplementedError

class Poll(wasi_poll.WasiPoll):
    def write_stream(self, stream: WasiStream, buf: bytes) -> Result[Size, StreamError]:
        raise NotImplementedError
 

def run() -> None:
    store = wasmtime.Store()

    wasm = Lists(store, ListsImports(
        imports=MyImports(),
        wasi_default_clocks=DefaultClock(),
        wasi_clocks=Clock(),
        wasi_logging=Logging(),
        wasi_filesystem=Filesystem(),
        wasi_poll=Poll(),
    ))

    allocated_bytes = wasm.allocated_bytes(store)
    wasm.test_imports(store)
    # assert(wasm.string_roundtrip(store, "x") == "x")
    # assert(wasm.string_roundtrip(store, "") == "")
    # assert(wasm.string_roundtrip(store, "hello ⚑ world") == "hello ⚑ world")

    # Ensure that we properly called `free` everywhere in all the glue that we
    # needed to.
    assert(allocated_bytes == wasm.allocated_bytes(store))

if __name__ == '__main__':
    run()
