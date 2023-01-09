#include "lists.h"


__attribute__((import_module("imports"), import_name("list-roundtrip")))
void __wasm_import_imports_list_roundtrip(int32_t, int32_t, int32_t);

__attribute__((import_module("imports"), import_name("string-roundtrip")))
void __wasm_import_imports_string_roundtrip(int32_t, int32_t, int32_t);
__attribute__((weak, export_name("cabi_post_list-roundtrip")))
void __wasm_export_lists_list_roundtrip_post_return(int32_t arg0) {
  int32_t ptr = *((int32_t*) (arg0 + 0));
  int32_t len = *((int32_t*) (arg0 + 4));
  for (int32_t i = 0; i < len; i++) {
    int32_t base = ptr + i * 1;
    (void) base;
  }
  if (len > 0) {
    free((void*) (ptr));
  }
}
__attribute__((weak, export_name("cabi_post_string-roundtrip")))
void __wasm_export_lists_string_roundtrip_post_return(int32_t arg0) {
  if ((*((int32_t*) (arg0 + 4))) > 0) {
    free((void*) (*((int32_t*) (arg0 + 0))));
  }
}

__attribute__((weak, export_name("cabi_realloc")))
void *cabi_realloc(void *ptr, size_t orig_size, size_t org_align, size_t new_size) {
  void *ret = realloc(ptr, new_size);
  if (!ret) abort();
  return ret;
}

// Helper Functions

void imports_list_u8_free(imports_list_u8_t *ptr) {
  if (ptr->len > 0) {
    free(ptr->ptr);
  }
}

void lists_list_u8_free(lists_list_u8_t *ptr) {
  if (ptr->len > 0) {
    free(ptr->ptr);
  }
}

void lists_string_set(lists_string_t *ret, const char*s) {
  ret->ptr = (char*) s;
  ret->len = strlen(s);
}

void lists_string_dup(lists_string_t *ret, const char*s) {
  ret->len = strlen(s);
  ret->ptr = cabi_realloc(NULL, 0, 1, ret->len * 1);
  memcpy(ret->ptr, s, ret->len * 1);
}

void lists_string_free(lists_string_t *ret) {
  if (ret->len > 0) {
    free(ret->ptr);
  }
  ret->ptr = NULL;
  ret->len = 0;
}

// Component Adapters

__attribute__((aligned(4)))
static uint8_t RET_AREA[8];

void imports_list_roundtrip(imports_list_u8_t *a, imports_list_u8_t *ret) {
  __attribute__((aligned(4)))
  uint8_t ret_area[8];
  int32_t ptr = (int32_t) &ret_area;
  __wasm_import_imports_list_roundtrip((int32_t) (*a).ptr, (int32_t) (*a).len, ptr);
  *ret = (imports_list_u8_t) { (uint8_t*)(*((int32_t*) (ptr + 0))), (size_t)(*((int32_t*) (ptr + 4))) };
}

void imports_string_roundtrip(lists_string_t *a, lists_string_t *ret) {
  __attribute__((aligned(4)))
  uint8_t ret_area[8];
  int32_t ptr = (int32_t) &ret_area;
  __wasm_import_imports_string_roundtrip((int32_t) (*a).ptr, (int32_t) (*a).len, ptr);
  *ret = (lists_string_t) { (char*)(*((int32_t*) (ptr + 0))), (size_t)(*((int32_t*) (ptr + 4))) };
}

__attribute__((export_name("test-imports")))
void __wasm_export_lists_test_imports(void) {
  lists_test_imports();
}

__attribute__((export_name("allocated-bytes")))
int32_t __wasm_export_lists_allocated_bytes(void) {
  uint32_t ret = lists_allocated_bytes();
  return (int32_t) (ret);
}

__attribute__((export_name("list-roundtrip")))
int32_t __wasm_export_lists_list_roundtrip(int32_t arg, int32_t arg0) {
  lists_list_u8_t arg1 = (lists_list_u8_t) { (uint8_t*)(arg), (size_t)(arg0) };
  lists_list_u8_t ret;
  lists_list_roundtrip(&arg1, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 4)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}

__attribute__((export_name("string-roundtrip")))
int32_t __wasm_export_lists_string_roundtrip(int32_t arg, int32_t arg0) {
  lists_string_t arg1 = (lists_string_t) { (char*)(arg), (size_t)(arg0) };
  lists_string_t ret;
  lists_string_roundtrip(&arg1, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 4)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}

extern void __component_type_object_force_link_lists(void);
void __component_type_object_force_link_lists_public_use_in_this_compilation_unit(void) {
  __component_type_object_force_link_lists();
}
