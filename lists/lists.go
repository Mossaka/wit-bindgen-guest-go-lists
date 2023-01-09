package lists

//#include "lists.h"
//#include <stdlib.h>
import "C"
import "unsafe"

// Exports
var exports Exports = nil

type Exports interface {
	ListsTestImports()
	ListsAllocatedBytes() uint32
	ListsListRoundtrip([]uint8) []uint8
	ListsStringRoundtrip(string) string
}

func SetExports(e Exports) {
	exports = e
}

//export lists_test_imports
func ListsTestImports() {
	exports.ListsTestImports()
}

//export lists_allocated_bytes
func ListsAllocatedBytes() C.uint32_t {
	return C.uint32_t(exports.ListsAllocatedBytes())
}

//export lists_list_roundtrip
func ListsListRoundtrip(param *C.lists_list_u8_t, ret *C.lists_list_u8_t) {
	// convert c param to go param
	var a []uint8
	if param.len == 0 {
		a = nil
	} else {
		a = (*[1 << 28]uint8)(unsafe.Pointer(param.ptr))[:param.len:param.len]
	}

	// call the function
	b := exports.ListsListRoundtrip(a)

	// convert go ret to c ret
	if len(b) == 0 {
		ret.ptr = nil
		ret.len = 0
	} else {
		ret.ptr = (*C.uint8_t)(unsafe.Pointer(&b[0]))
		ret.len = C.size_t(len(b))
	}
}

//export lists_string_roundtrip
func ListsStringRoundtrip(param *C.lists_string_t, ret *C.lists_string_t) {
	// convert c param to go param
	var a string = C.GoStringN(param.ptr, C.int(param.len))

	// call the function
	b := exports.ListsStringRoundtrip(a)

	// convert go ret to c ret
	ret.ptr = C.CString(b)
	ret.len = C.size_t(len(b))
}

// Imports
// void imports_list_roundtrip(imports_list_u8_t *a, imports_list_u8_t *ret0);
func ListRoundtrip(a []uint8) []uint8 {
	var l C.imports_list_u8_t
	var ret C.imports_list_u8_t

	// pass l_go to l, handle when a is nil.
	if len(a) == 0 {
		l.ptr = nil
		l.len = 0
	} else {
		l.ptr = (*C.uint8_t)(unsafe.Pointer(&a[0]))
		l.len = C.size_t(len(a))
	}

	// call the function
	C.imports_list_roundtrip(&l, &ret)

	// pass ret to ret_go of type []uint8
	// https://github.com/golang/go/wiki/cgo#turning-c-arrays-into-go-slices
	var theCArray *C.uint8_t = ret.ptr
	length := ret.len
	ret_go := (*[1 << 28]uint8)(unsafe.Pointer(theCArray))[:length:length]

	return ret_go

	//FIXME: do I need to free the memory?
}

func StringRoundtrip(a string) string {
	var c_param C.lists_string_t
	var c_ret C.lists_string_t

	// pass a to c_param of type lists_string_t
	c_param.ptr = C.CString(a)
	c_param.len = C.size_t(len(a))

	// call the function
	C.imports_string_roundtrip(&c_param, &c_ret)

	// pass c_ret to ret of type string
	var ret string = C.GoString(c_ret.ptr)
	return ret
}
