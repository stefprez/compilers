
class Parser:
    keywords = set(["auto", "break", "case", "char", "const", "continue",
                    "default", "do", "double", "else", "enum", "extern",
                    "float", "for", "goto", "if", "int", "long", "register",
                    "return", "short", "signed", "sizeof", "static", "struct",
                    "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while"])

    operators = set(["+", "-", "*", "/"])

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def is_keyword(input):
        return input in keywords
