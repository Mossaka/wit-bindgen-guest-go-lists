#include <stdlib.h>
#include <imports.h>

__attribute__((weak, export_name("cabi_realloc")))
void *cabi_realloc(
void *ptr,
size_t orig_size,
size_t org_align,
size_t new_size
) {
  void *ret = realloc(ptr, new_size);
  if (!ret)
  abort();
  return ret;
}
#include <string.h>

void imports_string_set(imports_string_t *ret, const char *s) {
  ret->ptr = (char*) s;
  ret->len = strlen(s);
}

void imports_string_dup(imports_string_t *ret, const char *s) {
  ret->len = strlen(s);
  ret->ptr = cabi_realloc(NULL, 0, 1, ret->len);
  memcpy(ret->ptr, s, ret->len);
}

void imports_string_free(imports_string_t *ret) {
  if (ret->len > 0) {
    free(ret->ptr);
  }
  ret->ptr = NULL;
  ret->len = 0;
}
void imports_list_u8_free(imports_list_u8_t *ptr) {
  if (ptr->len > 0) {
    free(ptr->ptr);
  }
}

__attribute__((aligned(4)))
static uint8_t RET_AREA[8];
__attribute__((import_module("imports"), import_name("list-roundtrip: func(a: list<u8>) -> list<u8>")))
void __wasm_import_imports_list_roundtrip(int32_t, int32_t, int32_t);
void imports_list_roundtrip(imports_list_u8_t *a, imports_list_u8_t *ret0) {
  int32_t ptr = (int32_t) &RET_AREA;
  __wasm_import_imports_list_roundtrip((int32_t) (*a).ptr, (int32_t) (*a).len, ptr);
  *ret0 = (imports_list_u8_t) { (uint8_t*)(*((int32_t*) (ptr + 0))), (size_t)(*((int32_t*) (ptr + 4))) };
}
__attribute__((import_module("imports"), import_name("string-roundtrip: func(a: string) -> string")))
void __wasm_import_imports_string_roundtrip(int32_t, int32_t, int32_t);
void imports_string_roundtrip(imports_string_t *a, imports_string_t *ret0) {
  int32_t ptr = (int32_t) &RET_AREA;
  __wasm_import_imports_string_roundtrip((int32_t) (*a).ptr, (int32_t) (*a).len, ptr);
  *ret0 = (imports_string_t) { (char*)(*((int32_t*) (ptr + 0))), (size_t)(*((int32_t*) (ptr + 4))) };
}
