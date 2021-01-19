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
        c = self.__peek_curr()
        start_pos = self.__pos + 1

        while c is not None:
            while c.isspace():
                c = self.__consume()

            print(c)

            if c == '"':
                tokens.append(self.__lex_string(start_pos))
            elif c.isalpha():
                tokens.append(self.__lex_word(start_pos))
            elif c.isdigit():
                tokens.append(self.__lex_number(start_pos))
            elif c in Genshi.SYMBOLS:
                print('SYMBOL!!!!')
                tokens.append(self.__lex_symbol(start_pos))
            else:
                raise SyntaxError(f"Unknown token starting with '{c}'")

            start_pos = self.__pos + 1
            c = self.__peek_curr()
        return tokens

    # Lex a string literal
    def __lex_string(self, start_pos):
        lexeme = ''
        c = self.__consume()

        while c != '"' and c is not None:
            lexeme += c
            c = self.__consume()
        return Token((start_pos, self.__pos - 1), Genshi.TT_STRING, lexeme)

    # Lex a numeric literal
    def __lex_number(self, start_pos):
        lexeme = ''
        c = self.__consume()
        is_float = False

        while c is not None:
            lexeme += c
            c = self.__consume()

            if c == '.' and not is_float:
                is_float = True
            elif c is None or not c.isdigit():
                break
        return Token((start_pos, self.__pos - 1), Genshi.TT_UFLOAT if is_float else Genshi.TT_UINT, lexeme)

    # Lex identifier or keyword
    def __lex_word(self, start_pos):
        lexeme = ''
        c = self.__consume()

        while c is not None:
            lexeme += c
            c = self.__consume()

            if c is None or not (c.isalnum() or c in ['_', '$']):
                break # exit if not valid identifier 

        tt = Genshi.KEYWORDS[lexeme] if lexeme in Genshi.KEYWORDS else Genshi.TT_IDENTIFIER
        return Token((start_pos, self.__pos - 1), tt, lexeme.upper())

    # Lex symbol (operator or syntax)
    def __lex_symbol(self, start_pos):
        lexeme = ''
        c1 = self.__consume()
        c2 = self.__peek_next()

        if c2 is not None and ((c1 + c2) in Genshi.SYMBOLS):
            c2 = self.__consume()
            lexeme = c1 + c2
        else:
            lexeme = c1
        return Token((start_pos, self.__pos - 1), Genshi.SYMBOLS[lexeme], lexeme)
            
    # Consume the next char in the statement (if anything is left)
    def __consume(self):
        c = self.__peek_curr()
        self.__pos += 1
        return c

    # Peek the current character
    def __peek_curr(self):
        if self.__pos >= len(self.__stmt):
            return None
        return self.__stmt[self.__pos]
    
    # Peek the next character to consume
    def __peek_next(self):
        n = self.__pos + 1
        return None if len(self.__stmt) <= n else self.__stmt[n]

    # Peek previous consumed character
    def __peek_prev(self):
        return None if self.__pos == 0 else self.__stmt[self.__pos - 1]
