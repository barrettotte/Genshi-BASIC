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
        c = self.__consume()

        while c:
            while c.isspace():
                c = self.__consume()
            if c == '"':
                tokens.append(self.__lex_string())
            elif c.isalpha():
                tokens.append(self.__lex_word())
            elif c.isdigit():
                tokens.append(self.__lex_number())
            elif c in Genshi.SYMBOLS:
                tokens.append(self.__lex_symbol())
            else:
                raise SyntaxError(f"Unknown token starting with '{c}'")
        return tokens

    # Lex a string literal
    def __lex_string(self):
        lexeme = ''
        c = self.__consume()
        while c != '"':
            lexeme += c
            c = self.__consume()
        return Token(self.__pos - 1, Genshi.TT_STRING, lexeme)

    # Lex a numeric literal
    def __lex_number(self):
        lexeme = ''
        is_float = False
        c = self.__peek_curr()

        while c:
            lexeme += c
            c = self.__consume()

            if c == '.' and not is_float:
                is_float = True
            elif not c.isdigit():
                break
        return Token(self.__pos, Genshi.TT_UFLOAT if is_float else Genshi.TT_UINT, lexeme)

    # Lex identifier or keyword
    def __lex_word(self):
        lexeme = ''
        c = self.__peek_curr()

        while c:
            lexeme += c
            c = self.__consume()
            if not (c.isalnum() or c in ['_', '$']):
                break # exit if not valid identifier 

        tt = Genshi.KEYWORDS[lexeme] if lexeme in Genshi.KEYWORDS else Genshi.TT_IDENTIFIER
        return Token(self.__pos, tt, lexeme)

    # Lex symbol (operator or syntax)
    def __lex_symbol(self):
        lexeme = ''
        c1 = self.__consume()
        c2 = self.__peek_next()

        if c2 and ((c1 + c2) in Genshi.SYMBOLS):
            c2 = self.__consume()
            lexeme = c1 + c2
        else:
            lexeme = c1
        return Token(self.__pos, Genshi.SYMBOLS[lexeme], lexeme)
            
    # Consume the next char in the statement (if anything is left)
    def __consume(self):
        if self.__pos >= len(self.__stmt):
            return None
        c = self.__stmt[self.__pos]
        self.__pos += 1
        return c

    # Peek the current character
    def __peek_curr(self):
        return self.__stmt[self.__pos]
    
    # Peek the next character to consume
    def __peek_next(self):
        n = self.__pos + 1
        return None if len(self.__stmt) <= n else self.__stmt[n]

    # Peek previous consumed character
    def __peek_prev(self):
        return None if self.__pos == 0 else self.__stmt[self.__pos - 1]
