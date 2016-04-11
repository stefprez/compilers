#! /usr/bin/env
import argparse

# mentions of id and number need to be changed to regex statements

parser = argparse.ArgumentParser(description='Interpreter for calculator.')
parser.add_argument('file_name', help='Filename of code.')
args = parser.parse_args()

file = open(args.file_name)
curr_token_queue = file.readline().split()
input_token = curr_token_queue.pop(0)
print input_token


def match(expected):
    global input_token
    if input_token == expected:
        input_token = curr_token_queue.pop(0)
        print input_token
    else:
        print_err("match")


def program():
    if input_token in ("id", "read", "write", "$$"):
        stmt_list()
        match("$$")
    else:
        print_err("program")


def stmt_list():
    if input_token in ("id", "read", "write"):
        stmt()
        stmt_list()
    elif input_token == "$$":
        pass
    else:
        print_err("stmt_list")


def stmt():
    if input_token == "id":
        match("id")
        match(":=")
        expr()
    elif input_token == "read":
        match("read")
        match("id")
    elif input_token == "write":
        match("write")
        expr()
    else:
        print_err("stmt")


def expr():
    if input_token in ("id", "number", "("):
        term()
        term_tail()
    else:
        print_err("expr")


def term_tail():
    if input_token in ("+", "-"):
        add_op()
        term()
        term_tail()
    elif input_token in (")", "id", "read", "write", "$$"):
        pass
    else:
        print_err("term_tail")


def term():
    if input_token in ("id", "number", "("):
        factor()
        factor_tail()
    else:
        print_err("term")


def factor_tail():
    if input_token in ("*", "/"):
        mult_op()
        factor()
        factor_tail()
    elif input_token in ("+", "-", ")", "id", "read", "write", "$$"):
        pass
    else:
        print_err("factor_tail")


def factor():
    if input_token == "id":
        match("id")
    elif input_token == "number":
        match("number")
    elif input_token == "(":
        match("(")
        expr()
        match(")")
    else:
        print_err("factor")


def add_op():
    if input_token == "+":
        match("+")
    elif input_token == "-":
        match("-")
    else:
        print_err("add_op")


def mult_op():
    if input_token == "*":
        match("*")
    elif input_token == "/":
        match("/")
    else:
        print_err("mult_op")


def print_err(func_name):
    print "Error in " + func_name


def main():
    program()


def get_next_token():
    pass

if __name__ == '__main__':
    main()
