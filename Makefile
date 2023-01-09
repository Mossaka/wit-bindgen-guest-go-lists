.PHONY: build
build:
	tinygo build -wasm-abi=generic -target=wasi -gc=leaking -no-debug -o lists.wasm main.go
	wasm-tools component new lists.wasm -o lists.wasm --adapt wasi_snapshot_preview1.wasm --wit world.wit
	python -m wasmtime.bindgen lists.wasm --out-dir host

test: build
	python host.py