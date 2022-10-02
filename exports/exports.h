#ifndef __BINDINGS_EXPORTS_H
#define __BINDINGS_EXPORTS_H
#ifdef __cplusplus
extern "C"
{
  #endif
  
  #include <stdint.h>
  #include <stdbool.h>
  
  typedef struct {
    char *ptr;
    size_t len;
  } exports_string_t;
  
  void exports_string_set(exports_string_t *ret, const char *s);
  void exports_string_dup(exports_string_t *ret, const char *s);
  void exports_string_free(exports_string_t *ret);
  typedef struct {
    uint8_t *ptr;
    size_t len;
  } exports_list_u8_t;
  void exports_list_u8_free(exports_list_u8_t *ptr);
  void exports_test_imports(void);
  uint32_t exports_allocated_bytes(void);
  void exports_list_roundtrip(exports_list_u8_t *a, exports_list_u8_t *ret0);
  void exports_string_roundtrip(exports_string_t *a, exports_string_t *ret0);
  #ifdef __cplusplus
}
#endif
#endif
