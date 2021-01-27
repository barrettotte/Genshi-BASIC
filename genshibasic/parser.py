# Parse list of tokens

from .stack import Stack
from .genshi import Genshi

class Parser:

    def __init__(self):
        self.__tok_idx = -1
        self.__tokens = []
        self.__line_no = -1
        self.__symbols = {}
        self.__op_stack = Stack()
        self.__pgm_data = []

    # parse token list and return syntax tree
    def parse(self, tokens, line_no):
        self.__tok_idx = 0
        self.__tokens = tokens
        self.__line_no = line_no
        self.__curr_tok = self.__tokens[self.__tok_idx]
