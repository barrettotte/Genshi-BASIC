# Building block for parser, created by the lexer

class Token:

    def __init__(self, col, tok_type, lexeme):
        self.col = col            # column index of token
        self.tok_type = tok_type  # type of token
        self.lexeme = lexeme      # contents scanned by lexer

    def __str__(self):
        return f'Column:{self.col}, Type:{self.tok_type}, Lexeme:{self.lexeme}'