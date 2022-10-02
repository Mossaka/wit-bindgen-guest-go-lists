package imports

//#include "imports.h"
//#include <stdlib.h>
import "C"
import "unsafe"

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
	var c_param C.imports_string_t
	var c_ret C.imports_string_t

	// pass a to c_param of type imports_string_t
	c_param.ptr = C.CString(a)
	c_param.len = C.size_t(len(a))

	// call the function
	C.imports_string_roundtrip(&c_param, &c_ret)

	// pass c_ret to ret of type string
	var ret string = C.GoString(c_ret.ptr)
	return ret
}
