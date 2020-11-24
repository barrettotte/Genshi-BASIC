# Building block for parser, created by the lexer

class Token:

    def __init__(self, pos, tok_type, lexeme):
        self.pos = pos            # starting position of token
        self.tok_type = tok_type  # type of token
        self.lexeme = lexeme      # contents scanned by lexer

    def __str__(self):
        return f'Position:{self.pos}, Type:{self.tok_type}, Lexeme:{self.lexeme}'