#ifndef __BINDINGS_IMPORTS_H
#define __BINDINGS_IMPORTS_H
#ifdef __cplusplus
extern "C"
{
  #endif
  
  #include <stdint.h>
  #include <stdbool.h>
  
  typedef struct {
    char *ptr;
    size_t len;
  } imports_string_t;
  
  void imports_string_set(imports_string_t *ret, const char *s);
  void imports_string_dup(imports_string_t *ret, const char *s);
  void imports_string_free(imports_string_t *ret);
  typedef struct {
    uint8_t *ptr;
    size_t len;
  } imports_list_u8_t;
  void imports_list_u8_free(imports_list_u8_t *ptr);
  void imports_list_roundtrip(imports_list_u8_t *a, imports_list_u8_t *ret0);
  void imports_string_roundtrip(imports_string_t *a, imports_string_t *ret0);
  #ifdef __cplusplus
}
#endif
#endif
