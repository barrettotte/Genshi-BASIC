# Parse list of tokens

from .token import Token

class Parser:

    def __init__(self):
        self.__symbols = {}  # symbol table

    # parse token list
    def parse(self, tokens, lineno):
        pass