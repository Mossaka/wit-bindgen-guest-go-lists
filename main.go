package main

import (
	"fmt"

	"github.com/mossaka/go-wit-bindgen-lists/lists"
)

func init() {
	lists.SetExports(ListsExportImpl{})
}

type ListsExportImpl struct{}

func (i ListsExportImpl) ListsTestImports() {
	lists.StringRoundtrip("x")

	res1 := lists.ListRoundtrip([]uint8{1, 2, 3})
	res2 := lists.StringRoundtrip("asdfasdf hello world")
	res3 := lists.StringRoundtrip("hello ⚑ world")
	res4 := lists.StringRoundtrip("")
	res5 := lists.ListRoundtrip([]uint8{})
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

func (ListsExportImpl) ListsAllocatedBytes() uint32 {
	return 0
}

func (i ListsExportImpl) ListsListRoundtrip(x []uint8) []uint8 {
	return x
}

func (i ListsExportImpl) ListsStringRoundtrip(x string) string {
	return x
}

func main() {
}
