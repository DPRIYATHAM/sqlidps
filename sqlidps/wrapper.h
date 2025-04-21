#ifndef MYSQL_LEXER_PY_H
#define MYSQL_LEXER_PY_H

#ifdef __cplusplus
extern "C" {
#endif

/* Function called by the lexer to record a token name */
void append_token(const char* token_name);

#ifdef __cplusplus
}
#endif

#endif
