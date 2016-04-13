#! /usr/bin/env
import argparse
import re
import sys

# Usage
# From command line, `python /path/to/interpreter.py /path/to/your_file.txt`

# Set up command line arguments
parser = argparse.ArgumentParser(description='Interpreter for calculator.')
parser.add_argument('file_name', help='Filename of code.')
args = parser.parse_args()

# Open passed in file
file = open(args.file_name)

# Initialize global variables
curr_token_queue = []
input_token = ""
curr_line_num = 0
curr_line = ""
token_position = 0


def match(expected):
    if input_token == expected:
        get_next_token()
    else:
        print_err("match()", expected)


def program():
    if input_token in ("read", "write", "$$") or token_is_id():
        stmt_list()
        match("$$")
    else:
        print_err("program()")


def stmt_list():
    if input_token in ("read", "write") or token_is_id():
        stmt()
        stmt_list()
    elif input_token == "$$":
        pass
    else:
        print_err("stmt_list()")


def stmt():
    if token_is_id():
        match(input_token)
        match(":=")
        expr()
    elif input_token == "read":
        match("read")
        match(input_token)
    elif input_token == "write":
        match("write")
        expr()
    else:
        print_err("stmt()")


def expr():
    if input_token == "(" or token_is_id() or token_is_num():
        term()
        term_tail()
    else:
        print_err("expr()")


def term_tail():
    if input_token in ("+", "-"):
        add_op()
        term()
        term_tail()
    elif input_token in (")", "read", "write", "$$") or token_is_id():
        pass
    else:
        print_err("term_tail()")


def term():
    if input_token == "(" or token_is_id() or token_is_num():
        factor()
        factor_tail()
    else:
        print_err("term()")


def factor_tail():
    if input_token in ("*", "/"):
        mult_op()
        factor()
        factor_tail()
    elif input_token in ("+", "-", ")",
                         "read", "write", "$$") or token_is_id():
        pass
    else:
        print_err("factor_tail()")


def factor():
    if token_is_id() or token_is_num():
        match(input_token)
    elif input_token == "(":
        match("(")
        expr()
        match(")")
    else:
        print_err("factor()")


def add_op():
    if input_token == "+":
        match("+")
    elif input_token == "-":
        match("-")
    else:
        print_err("add_op()")


def mult_op():
    if input_token == "*":
        match("*")
    elif input_token == "/":
        match("/")
    else:
        print_err("mult_op()")


def print_err(func_name, expected=None):
    print "Error in " + func_name

    if expected is None:
        # Parser Error
        print "Parser error on line {0}".format(curr_line_num)
    else:
        # Tokenizer Error
        print "Tokenizer error on line {0}: Expected '{1}'".format(curr_line_num, expected)

    # Print line with error
    print curr_line.rstrip()

    print_error_pointer()
    sys.exit(1)


def print_error_pointer():
    error_pointer_string = ""

    # Pad with whitespace to position pointer
    for _ in range(0, token_position):
        error_pointer_string += " "

    error_pointer_string += "^"

    print error_pointer_string


def main():
    get_next_token()
    program()


def get_next_token():
    # Access global variables
    global curr_token_queue
    global input_token
    global curr_line_num
    global curr_line
    global token_position

    # Check if current token queue is empty
    if not curr_token_queue:
        # Queue is empty

        # Read in next line
        curr_line = file.readline()

        # Separate line into separate tokens
        curr_token_queue = re.findall(':=|\w+|[()]|\+|\-|\*|\/|\$\$$|\S',
                                      curr_line)

        # Check for end of file
        if not curr_token_queue:
            if input_token == "$$":
                print "Valid file!"
                sys.exit(0)
            else:
                print "Error: Missing $$ at end of file."
                sys.exit(1)

        # Update counters
        curr_line_num += 1
        token_position = 0
        input_token = ""

    # Keep counter of current token position
    if input_token:
        token_position += len(input_token) + 1

    # Get next input_token from queue
    input_token = curr_token_queue.pop(0)


def token_is_id():
    # Check if input_token is an alphabetical ID and not read or write
    return re.match('^(?!read|write)[A-Za-z]+$', input_token)


def token_is_num():
    # Check if input_token is a number
    return re.match('^\d+$', input_token)


if __name__ == '__main__':
    main()
