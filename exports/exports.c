#include <stdlib.h>
#include <exports.h>

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

void exports_string_set(exports_string_t *ret, const char *s) {
  ret->ptr = (char*) s;
  ret->len = strlen(s);
}

void exports_string_dup(exports_string_t *ret, const char *s) {
  ret->len = strlen(s);
  ret->ptr = cabi_realloc(NULL, 0, 1, ret->len);
  memcpy(ret->ptr, s, ret->len);
}

void exports_string_free(exports_string_t *ret) {
  if (ret->len > 0) {
    free(ret->ptr);
  }
  ret->ptr = NULL;
  ret->len = 0;
}
void exports_list_u8_free(exports_list_u8_t *ptr) {
  if (ptr->len > 0) {
    free(ptr->ptr);
  }
}

__attribute__((aligned(4)))
static uint8_t RET_AREA[8];
__attribute__((export_name("test-imports: func() -> ()")))
void __wasm_export_exports_test_imports(void) {
  exports_test_imports();
}
__attribute__((export_name("allocated-bytes: func() -> u32")))
int32_t __wasm_export_exports_allocated_bytes(void) {
  uint32_t ret = exports_allocated_bytes();
  return (int32_t) (ret);
}
__attribute__((export_name("list-roundtrip: func(a: list<u8>) -> list<u8>")))
int32_t __wasm_export_exports_list_roundtrip(int32_t arg, int32_t arg0) {
  exports_list_u8_t arg1 = (exports_list_u8_t) { (uint8_t*)(arg), (size_t)(arg0) };
  exports_list_u8_t ret;
  exports_list_roundtrip(&arg1, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 4)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}
__attribute__((export_name("cabi_post_list-roundtrip")))
void __wasm_export_exports_list_roundtrip_post_return(int32_t arg0) {
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
__attribute__((export_name("string-roundtrip: func(a: string) -> string")))
int32_t __wasm_export_exports_string_roundtrip(int32_t arg, int32_t arg0) {
  exports_string_t arg1 = (exports_string_t) { (char*)(arg), (size_t)(arg0) };
  exports_string_t ret;
  exports_string_roundtrip(&arg1, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 4)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}
__attribute__((export_name("cabi_post_string-roundtrip")))
void __wasm_export_exports_string_roundtrip_post_return(int32_t arg0) {
  if ((*((int32_t*) (arg0 + 4))) > 0) {
    free((void*) (*((int32_t*) (arg0 + 0))));
  }
}
