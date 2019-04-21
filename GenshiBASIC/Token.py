class Token:

    def __init__(self, token_type=None, lexeme=None, line=None, literal=None, pos=None):
        self.token_type = '' if token_type is None else token_type
        self.lexeme = '' if lexeme is None else lexeme
        self.literal = literal
        self.line = -1 if line is None else line
        self.pos = (0,0) if pos is None else pos

    def __str__(self):
        s = { 
          "type": self.token_type, 
          "lexeme": str(self.lexeme), 
          "literal": str(self.literal),
          "line": str(self.line), 
          "pos": str(self.pos),
        }
        return str(s)
        