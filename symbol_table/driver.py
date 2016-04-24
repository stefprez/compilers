import argparse
from symbol_table import *
from parser import *


def main():
    # Setup Command Line Arguments
    arg_parser = argparse.ArgumentParser(description='Symbol Table creator')
    arg_parser.add_argument('file_name', help='Filename of input code.')
    args = arg_parser.parse_args()  

    # Initialize Symbol Table and Parser
    symbol_table = SymbolTable()
    parser = Parser(symbol_table)
   
    # Parse input file
    parser.parse_file(args.file_name)
        
    # Print Symbol Table
    symbol_table.print_table()


if __name__ == "__main__":
    main()

