#ifndef __BINDINGS_LISTS_H
#define __BINDINGS_LISTS_H
#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
  char*ptr;
  size_t len;
} lists_string_t;

typedef struct {
  uint8_t *ptr;
  size_t len;
} imports_list_u8_t;

typedef struct {
  uint8_t *ptr;
  size_t len;
} lists_list_u8_t;

// Imported Functions from `imports`
void imports_list_roundtrip(imports_list_u8_t *a, imports_list_u8_t *ret);
void imports_string_roundtrip(lists_string_t *a, lists_string_t *ret);

// Exported Functions from `lists`
void lists_test_imports(void);
uint32_t lists_allocated_bytes(void);
void lists_list_roundtrip(lists_list_u8_t *a, lists_list_u8_t *ret);
void lists_string_roundtrip(lists_string_t *a, lists_string_t *ret);

// Helper Functions

void imports_list_u8_free(imports_list_u8_t *ptr);
void lists_list_u8_free(lists_list_u8_t *ptr);
void lists_string_set(lists_string_t *ret, const char*s);
void lists_string_dup(lists_string_t *ret, const char*s);
void lists_string_free(lists_string_t *ret);

#ifdef __cplusplus
}
#endif
#endif
