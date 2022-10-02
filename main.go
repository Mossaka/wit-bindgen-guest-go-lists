package main

import (
	// "github.com/mossaka/go-wit-bindgen-lists/exports"

	"fmt"

	"github.com/mossaka/go-wit-bindgen-lists/exports"
	"github.com/mossaka/go-wit-bindgen-lists/imports"
)

func init() {
	exports.SetExports(ListsExportImpl{})
}

type ListsExportImpl struct{}

func (i ListsExportImpl) TestImports() {
	imports.StringRoundtrip("x")

	res1 := imports.ListRoundtrip([]uint8{1, 2, 3})
	res2 := imports.StringRoundtrip("asdfasdf hello world")
	res3 := imports.StringRoundtrip("hello ⚑ world")
	res4 := imports.StringRoundtrip("")
	res5 := imports.ListRoundtrip([]uint8{})
	if string(res1) != string([]uint8{1, 2, 3}) {
		panic(fmt.Sprintf("res1 = %v", res1))
	}
	if res2 != "asdfasdf hello world" {
		panic(fmt.Sprintf("res2 = %v", res2))
	}
	if res3 != "hello ⚑ world" {
		panic(fmt.Sprintf("res3 = %v", res3))
	}
	if res4 != "" {
		panic(fmt.Sprintf("res4 = %v", res4))
	}
	if len(res5) != 0 {
		panic(fmt.Sprintf("res5 = %v", res5))
	}
}

func (ListsExportImpl) AllocatedBytes() uint32 {
	return 0
}

func (i ListsExportImpl) ListRoundtrip(x []uint8) []uint8 {
	return x
}

func (i ListsExportImpl) StringRoundtrip(x string) string {
	return x
}

func main() {
}
