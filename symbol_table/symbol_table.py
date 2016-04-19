# types = ["int", "char", "[]int", "[]char", "*int", "*char"]

# keywords = ["auto", "break", "case", "char", "const", "continue", "default",
#             "do", "double", "else", "enum", "extern", "float", "for", "goto",
#             "if", "int", "long", "register", "return", "short", "signed",
#             "sizeof", "static", "struct", "switch", "typedef", "union",
#             "unsigned", "void", "volatile", "while"]


class SymbolTable:

    def __init__(self):
        self.primitives = []
        self.functions = []
        self.arrays = []
        self.pointers = []

    def print_table():
        print "Symbol Table"
        print "#" * 25
        print

        print "**Primitive Variables**"
        for primitive in self.primitives:
            print "Name: {0}".format(primitive.name)
            print "Type: {0}".format(primitive.var_type)
            print "Procedure Name: {0}".format(primitive.proc_name)
            print "Lexical Level: {0}".format(primitive.lex_level)
            print "Line Counter: {0}".format(primitive.line_num)
            print

        print "**Functions**"
        for function in self.functions:
            print "Name: {0}".format(function.name)
            print "Number of Parameters: {0}".format(function.num_params)
            for i, parameter in enumerate(function.parameters, start=1):
                print "Parameter {0}".format(i)
                print "Parameter Name: {0}".format(parameter.name)
                print "Parameter Type: {0}".format(parameter.param_type)
            print "Return Value Type: {0}".format(function.return_type)
            print "Line Counter: {0}".format(function.line_num)
            print

        print "**Array Variables**"
        for array in self.arrays:
            print "Name: {0}".format(array.name)
            print "Type: {0}".format(array.var_type)
            print "Procedure Name: {0}".format(array.proc_name)
            print "Lexical Level: {0}".format(array.lex_level)
            print "Number of Dimensions: {0}".format(array.num_dims)
            for i, dimension in enumerate(array.dimensions, start=1):
                print "Dimension {0}".format(i)
                print "Upper Bound: {0}".format(dimension.upper_bound)
            print "Line Counter: {0}".format(array.line_num)
            print

        print "**Pointers**"
        for pointer in self.pointers:
            print "Name: {0}".format(pointer.name)
            print "Dereferenced Type: {0}".format(pointer.deref_type)
            print "Procedure Name: {0}".format(pointer.proc_name)
            print "Lexical Level: {0}".format(pointer.lex_level)
            print "Line Counter: {0}".format(pointer.line_num)
            print

        print "#" * 25


class PrimitiveVariable:

    def __init__(self, name, var_type, proc_name, lex_level, line_num):
        self.name = name
        self.var_type = var_type
        self.proc_name = proc_name
        self.lex_level = lex_level
        self.line_num = line_num


class Function:

    def __init__(self, name, parameters, return_type, line_num):
        self.name = name
        self.parameters = parameters
        self.num_params = len(parameters)
        self.return_type = return_type
        self.line_num = line_num


class Parameter:

    def __init__(self, name, param_type):
        self.name = name
        self.param_type = param_type


class ArrayVariable:

    def __init__(self, name, arr_type, proc_name, lex_level, dimensions,
                 line_num):
        self.name = name
        self.arr_type = arr_type
        self.proc_name = proc_name
        self.lex_level = lex_level
        self.dimensions = dimensions
        self.num_dims = len(dimensions)
        self.line_num = line_num


class Dimension:

    def __init__(self, upper_bound):
        self.upper_bound = upper_bound


class Pointer:

    def __init__(self, name, deref_type, proc_name, lex_level, line_num):
        self.name = name
        self.deref_type = deref_type
        self.proc_name = proc_name
        self.lex_level = lex_level
        self.line_num = line_num
