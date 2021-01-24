# Building block for parser, created by the lexer

class Token:

    def __init__(self, pos, tok_type, lexeme):
        if type(pos) is not tuple:
            raise TypeError(f"Expected pos of type tuple, but got {type(pos)}")

        self.pos = pos            # tuple of start/end pos
        self.tok_type = tok_type  # type of token
        self.lexeme = lexeme      # contents scanned by lexer

    def __str__(self):
        s = f"Position=({self.pos[0]}:{self.pos[1]})"
        s += f", Type={self.tok_type}"
        s += f", 'Lexeme={self.lexeme}'"
        return s
