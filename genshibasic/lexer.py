# The lexer scans a genshi BASIC statement and breaks it into a list of tokens

from .token import Token

class Lexer:

    def __init__(self):
        self.col = 0
        self.stmt = None

    # scan statement and build list of tokens
    def lex(self, stmt):
        tokens = []
        self.stmt = stmt
        self.col = 0
        c = self.consume()

    # Consume the next char in the statement (if anything is left)
    def consume(self):
        if self.col >= len(self.stmt):
            return None
        c = self.stmt[self.col]
        self.col += 1
        return c