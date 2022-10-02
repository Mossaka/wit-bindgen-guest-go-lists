package exports

// #include "exports.h"
import "C"
import "unsafe"

var exports Exports = nil

type Exports interface {
	TestImports()
	AllocatedBytes() uint32
	ListRoundtrip([]uint8) []uint8
	StringRoundtrip(string) string
}

func SetExports(e Exports) {
	exports = e
}

//export exports_test_imports
func TestImports() {
	exports.TestImports()
}

//export exports_allocated_bytes
func AllocatedBytes() C.uint32_t {
	return C.uint32_t(exports.AllocatedBytes())
}

//export exports_list_roundtrip
func ListRoundtrip(param *C.exports_list_u8_t, ret *C.exports_list_u8_t) {
	// convert c param to go param
	var a []uint8
	if param.len == 0 {
		a = nil
	} else {
		a = (*[1 << 28]uint8)(unsafe.Pointer(param.ptr))[:param.len:param.len]
	}

	// call the function
	b := exports.ListRoundtrip(a)

	// convert go ret to c ret
	if len(b) == 0 {
		ret.ptr = nil
		ret.len = 0
	} else {
		ret.ptr = (*C.uint8_t)(unsafe.Pointer(&b[0]))
		ret.len = C.size_t(len(b))
	}
}

//export exports_string_roundtrip
func StringRoundtrip(param *C.exports_string_t, ret *C.exports_string_t) {
	// convert c param to go param
	var a string = C.GoStringN(param.ptr, C.int(param.len))

	// call the function
	b := exports.StringRoundtrip(a)

	// convert go ret to c ret
	ret.ptr = C.CString(b)
	ret.len = C.size_t(len(b))
}
