import symbol_table
import re
from symbol_table import *

class Parser:
    keywords = set(["auto", "break", "case", "char", "const", "continue",
                    "default", "do", "else", "extern",
                    "for", "goto", "if", "int", "register",
                    "return", "signed", "sizeof", "static", "struct",
                    "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while"])

    operators = set(["+", "-", "*", "/"])

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.lexical_level = "global"
        self.line_num = 0
        self.curr_line = ""

    def is_keyword(self, word):
        return word in Parser.keywords

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
            # parse_word(word)
            if self.is_keyword(word):
                if self.is_type(word):
                    self.process_declaration(words)
                    break

    def process_declaration(self, words):
        for i, word in enumerate(words):
            if self.is_type(word):
                if self.is_function(words[i + 1]):
                    self.process_function()
                else:
                    self.process_variable(words)

    def process_function(self):
        regex_match = re.search("(\w+) (\w+)\((.*)\)", self.curr_line)
        return_type = regex_match.group(1)
        func_name = regex_match.group(2)
        param_list = regex_match.group(3)
        params = self.parse_param_list(param_list)
        
        self.symbol_table.add(Function(func_name, params, return_type,
            self.line_num))
        
    def process_variable(self, words):
        pass
        
    def parse_param_list(self, param_list):
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

    def is_pointer(self, word):
        return word[0] == "*"

    def is_array(self, word):
        return word[-1] == "]"

    # def parse_word(word):
        # if is_keyword(word):

