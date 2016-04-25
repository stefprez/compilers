import symbol_table
import re
from symbol_table import *

class Parser:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.lexical_level = [0 for _ in range(0, 32)]
        self.lex_counter = 0 
        self.line_num = 0
        self.curr_line = ""
        self.curr_proc = "None"
        self.bracket_stack = []

    def parse_file(self, input_file):
        with open(input_file) as input_file:
            for line in input_file:
                self.line_num += 1
                self.curr_line = line
                self.parse_line(line)

    def get_symbol_table(self):
        return self.symbol_table

    def parse_line(self, line):
        words = line.split()

        for word in words:
            if self.is_type(word):
                self.process_declaration(words)
                break
            elif word == "{":
                # New lexical level
                self.push()
            elif word == "}":
                # End of lexical level
                self.pop()

    def process_declaration(self, words):
        for i, word in enumerate(words):
            if self.is_type(word):
                if self.is_function(words[i + 1]):
                    self.process_function()
                else:
                    self.process_variable()
                break

    def process_function(self):
        # Use regex to find return type, function name, and parameter list
        regex_match = re.search("(\w+) (\w+)\((.*)\)", self.curr_line)

        return_type = regex_match.group(1)
        func_name = regex_match.group(2)
        param_list = regex_match.group(3)

        # Correctly parse parameter list
        params = self.parse_param_list(param_list)
        
        # Build new Function object and add it to the symbol table
        self.symbol_table.add(Function(func_name, params, return_type,
            self.line_num))
        
        # Set current procedure
        self.curr_proc = func_name
        self.lexical_level[0] = self.lex_counter
        self.push()
        self.lex_counter += 1
        
    def process_variable(self):
        # Use regex to find variable type and variable names
        regex_match = re.search("(int|char) (.+);", self.curr_line)
        primitive_type = regex_match.group(1)
        var_names, var_types = self.parse_var_names(regex_match.group(2))

        for i, var_type in enumerate(var_types):
            if var_type is PrimitiveVariable:
                # Add new PrimitiveVariable to Symbol Table
                self.symbol_table.add(PrimitiveVariable(var_names[i],
                    primitive_type, self.curr_proc, self.get_lexical_level(), self.line_num))  
            elif var_type is Pointer:
                # Add new Pointer to Symbol Table
                self.symbol_table.add(Pointer(var_names[i], primitive_type,
                self.curr_proc, self.get_lexical_level(), self.line_num))
            elif var_type is ArrayVariable:
                # Add new ArrayVariable to Symbol Table
                dimensions, arr_name = self.process_dims(var_names[i])
                self.symbol_table.add(ArrayVariable(arr_name,
                    primitive_type, self.curr_proc, self.get_lexical_level(), dimensions, self.line_num))

    def process_dims(self, raw_name):
        # Get correct array name and dimension values
        name_and_dims_list = raw_name.split('[')                 
        arr_name = name_and_dims_list[0]
        dims = []

        for dim in name_and_dims_list[1:]:
            dim_limit = int(dim[0])
            dims.append(Dimension(dim_limit))

        return dims, arr_name

    def push(self):
        self.bracket_stack.append("{")
        self.increment_lexical_level()

    def pop(self):
        self.bracket_stack.pop()
        self.decrement_lexical_level()
        if len(self.bracket_stack) == 0:
            # Outside of a function
            self.lexical_level[0] = 0
            self.curr_proc = "None"
    
    def increment_lexical_level(self):
        index = len(self.bracket_stack) - 1
        self.lexical_level[index] += 1
    
    def decrement_lexical_level(self):
        index = len(self.bracket_stack) + 1
        self.lexical_level[index] = 0

    def get_lexical_level(self):
        # Get lexical level string representation
        if self.lexical_level[0] == 0:
            return "global"
        else:
            index = 1
            return_level = str(self.lexical_level[0])
            while self.lexical_level[index] > 0:
                return_level += "." + str(self.lexical_level[index])
                index += 1
            return return_level

    def parse_var_names(self, raw_var_names):
        # Parse variable names and types if mixed on line
        raw_var_names = raw_var_names.split(",")
        var_types = []
        var_names = []
        
        for var_name in raw_var_names:
            if "=" in var_name:
                # Strip out initialization from variable name
                var_name = var_name[:var_name.index("=") - 1]
            var_names.append(var_name)

            if "*" in var_name:
                # Pointer
                var_types.append(Pointer)
            elif "[" in var_name:
                # Array
                var_types.append(ArrayVariable)
            else:
                # Primitive
                var_types.append(PrimitiveVariable)

        return var_names, var_types

    def parse_param_list(self, param_list):
        # Process the string of parameters into separate parameter objects

        if not param_list:
            return []

        raw_params = param_list.split(',')
        params = []
        
        for param in raw_params:
            param_type, param_name = param.split()
            params.append(Parameter(param_name, param_type))
                        
        return params

    def is_function(self, word):
        return "(" in word

    def is_type(self, word):
        return word in set(["int", "char", "void"])

