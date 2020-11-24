# The lexer scans a genshi BASIC statement and breaks it into a list of tokens

from .token import Token
from .definitions import TokenType

class Lexer:

    def __init__(self):
        self.__pos = 0
        self.__stmt = None

    # scan statement and build list of tokens
    def lex(self, stmt):
        tokens = []
        self.__pos = 0
        self.__stmt = stmt

        c = self.__consume()
        while c:
            while c.isspace():
                c = self.__consume()

            if c == '"':
                tokens.append(self.__lex_string())
            elif c.isalpha():
                pass
            elif c.isdigit():
                tokens.append(self.__lex_number())
            else:
                raise SyntaxError("Unknown token")
        return tokens

    # Lex a string literal
    def __lex_string(self):
        lexeme = ''
        c = self.__consume()
        while c != '"':
            lexeme += c
            c = self.__consume()
        return Token(self.__pos-1, TokenType.STRING, lexeme)

    # Lex a numeric literal
    def __lex_number(self):
        lexeme = ''
        is_float = False
        c = self.__curr_char()

        while True:
            lexeme += c
            c = self.__consume()

            if c == '.' and not is_float:
                is_float = True
            elif not c.isdigit():
                break
    
        return Token(self.__pos, TokenType.UFLOAT if is_float else TokenType.UINT, lexeme)



    # Consume the next char in the statement (if anything is left)
    def __consume(self):
        if self.__pos >= len(self.__stmt):
            return None
        c = self.__stmt[self.__pos]
        self.__pos += 1
        return c

    # Get current character
    def __curr_char(self):
        return self.__stmt[self.__pos]