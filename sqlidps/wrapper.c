#include "./wrapper.h" /* Ensure this header declares append_token() if needed */
#include <Python.h>

/* Declarations for Flex’s scanning functions */
extern int yylex(void);
extern void *yy_scan_string(const char *s);
extern void yy_delete_buffer(void *buf);

/* Global variable to hold the Python list of token names */
static PyObject *token_list = NULL;

/* This function is called from the Lex rules to append a token name */
void append_token(const char *token_name) {
  if (token_list) {
    PyObject *py_token = PyUnicode_FromString(token_name);
    PyList_Append(token_list, py_token);
    Py_DECREF(py_token);
  }
}

/* Python wrapper for the lexer.
   Accepts a string and returns a list of token names. */
static PyObject *py_tokenize(PyObject *self, PyObject *args) {
  const char *input;
  if (!PyArg_ParseTuple(args, "s", &input))
    return NULL;

  /* Create a new Python list to hold token names */
  token_list = PyList_New(0);

  /* Initialize the Flex buffer with the input string */
  void *buffer = yy_scan_string(input);

  /* Run the lexer */
  yylex();

  /* Clean up the Flex buffer */
  yy_delete_buffer(buffer);

  /* Save the list to return, and reset our global pointer */
  PyObject *result = token_list;
  token_list = NULL;
  return result;
}

/* Define module methods */
static PyMethodDef LexerMethods[] = {
    {"tokenize", py_tokenize, METH_VARARGS,
     "Tokenize a MySQL query string and return a list of token names."},
    {NULL, NULL, 0, NULL}};

/* Module definition with module name "token" */
static struct PyModuleDef token_module = {
    PyModuleDef_HEAD_INIT, "sql_tokenizer", /* Module name */
    "MySQL Lexer Module", -1, LexerMethods};

/* Module initialization function */
PyMODINIT_FUNC PyInit_sql_tokenizer(void) {
  return PyModule_Create(&token_module);
}
