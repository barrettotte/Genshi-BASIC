# The lexer scans a genshi BASIC statement and breaks it into a list of tokens

from .token import Token

class Lexer:

    def __init__(self):
        self.__col = 0
        self.__stmt = None

    # scan statement and build list of tokens
    def lex(self, stmt):
        tokens = []
        self.__col = 0
        self.__stmt = stmt
        c = self.__consume()

    # Consume the next char in the statement (if anything is left)
    def __consume(self):
        if self.__col >= len(self.__stmt):
            return None
        c = self.__stmt[self.__col]
        self.__col += 1
        return c