//Remember that this is CPP code that is callable
//I'm comparing between the hand written method and the tool generated methods


//First, write a Python-callable function that takes in a string and returns a string.

static PyObject * hello_wrapper(PyObject * self, PyObject * args)
{
  char * input;
  char * result;
  PyObject * ret;

  // parse arguments
  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  // run the actual function
  result = hello(input);

  // build the resulting string into a Python object.
  ret = PyString_FromString(result);
  free(result);

  return ret;
}

//Second, register this function within a module’s symbol table
//(all Python functions live in a module, even if they’re actually C functions!)

static PyMethodDef HelloMethods[] = {
 { "hello", hello_wrapper, METH_VARARGS, "Say hello" },
 { NULL, NULL, 0, NULL }
};

//Third, write an init function for the module (all extension modules require an init function).
DL_EXPORT(void) inithello(void)
{
  Py_InitModule("hello", HelloMethods);
}

