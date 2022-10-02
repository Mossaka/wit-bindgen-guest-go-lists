
.PHONY: install
install:
	cargo install wit-bindgen-cli --git  https://github.com/mossaka/wit-bindgen --branch go-guest-new

.PHONY: gen
gen:
	mkdir imports
	cd imports && wit-bindgen guest c -i ../imports.wit && wit-bindgen guest go -i ../imports.wit 
	mkdir exports
	cd exports && wit-bindgen guest c -e ../exports.wit && wit-bindgen guest go -e ../exports.wit 
	cd host && wit-bindgen host wasmtime-py -e ../imports.wit && mv bindings.py imports.py && wit-bindgen host wasmtime-py -i ../exports.wit && mv bindings.py exports.py


.PHONY: build
build: gen
	tinygo build -wasm-abi=generic -target=wasi -gc=leaking -no-debug -o main.wasm main.go

.PHONY: clean
clean:
	rm -r imports
	rm -r exports