# The lexer scans a genshi BASIC statement and breaks it into a list of tokens

from .token import Token
from .genshi import Genshi


class Lexer:

    def __init__(self):
        self.__pos = 0
        self.__stmt = None

    # Scan statement and build list of tokens
    def lex(self, stmt):
        tokens = []
        self.__pos = 0
        self.__stmt = stmt
        c = self.__peek()

        while c is not None:
            # eat all blanks
            while c.isspace():
                c = self.__consume()
                if not c.isspace():
                    self.__rewind()
                    break
            start_pos = self.__pos + 1

            if c == '"':
                t = self.__lex_string(start_pos)
            elif c.isalpha():
                t = self.__lex_word(start_pos)
            elif c.isdigit():
                t = self.__lex_number(start_pos)
            elif c in Genshi.SYMBOLS:
                t = self.__lex_symbol(start_pos)
            else:
                raise SyntaxError(f"Unknown token starting with '{c}'")

            tokens.append(t)
            c = self.__peek()
        return tokens

    # Lex a string literal
    def __lex_string(self, start_pos):
        lexeme = self.__consume()
        c = self.__consume()

        while c is not None:
            if c == '"':
                lexeme += c
                break
            lexeme += c
            c = self.__consume()
        return Token((start_pos, self.__pos), Genshi.TT_STRING, lexeme)

    # Lex a numeric literal
    def __lex_number(self, start_pos):
        lexeme = ''
        c = self.__consume()
        is_float = False

        while c is not None:
            if not c.isdigit():
                if c == '.' and not is_float:
                    is_float = True
                else:
                    self.__rewind()
                    break
            lexeme += c
            c = self.__consume()
        tt = Genshi.TT_UFLOAT if is_float else Genshi.TT_UINT
        return Token((start_pos, self.__pos), tt, lexeme)

    # Lex identifier or keyword
    def __lex_word(self, start_pos):
        lexeme = ''
        c = self.__consume()

        while c is not None:
            if not (c.isalnum() or c in ['_', '$']):
                self.__rewind()
                break
            lexeme += c
            c = self.__consume()

        if lexeme in Genshi.KEYWORDS:
            tt = Genshi.KEYWORDS[lexeme]
        else:
            tt = Genshi.TT_IDENTIFIER
        return Token((start_pos, self.__pos), tt, lexeme.upper())

    # Lex symbol (operator or syntax)
    def __lex_symbol(self, start_pos):
        c = self.__consume()

        if c is not None and ((c + self.__peek()) in Genshi.SYMBOLS):
            lexeme = c + self.__consume()  # two char symbol
        else:
            lexeme = c
        return Token((start_pos, self.__pos), Genshi.SYMBOLS[lexeme], lexeme)

    # Consume the next char in the statement (if anything is left)
    def __consume(self):
        c = self.__peek()
        self.__pos += 1 if c is not None else 0
        return c

    # Rewind back a character
    def __rewind(self):
        self.__pos -= 1 if self.__pos > 0 else 0

    # Peek the current character
    def __peek(self):
        if self.__pos >= len(self.__stmt):
            return None
        return self.__stmt[self.__pos]
