from GenshiBASIC.Token import Token


class Expression:
    def __init__(self): pass
    def __str__(self):  return "Base expression object"


class Literal(Expression):
    def __init__(self, literal_token):
        if not type(literal_token) is Token: raise TypeError("Literal token must be of type Token")
        self.val = literal_token
    
    def __str__(self):
        return str(self.val)


class Grouping(Expression):
    def __init__(self, left_paren, exp, right_paren):
        if not type(left_paren) is Token:  raise TypeError("Left paren must be of type Token")
        if not type(exp) is Expression:    raise TypeError("Expression must be of type Expression")
        if not type(right_paren) is Token: raise TypeError("Right paren must be of type Token")
        self.left_paren = left_paren
        self.exp = exp
        self.right_paren = right_paren

    def __str__(self):
        return "( " + str(self.exp) + " )"


class Unary(Expression):
    def __init__(self, op_token, exp):
        if not type(op_token)  is Token: raise TypeError("Operator token must be of type Token")
        if not type(exp) is Expression:  raise TypeError("Expression must be of type Expression")
        self.op_token = op_token
        self.exp = exp

    def __str__(self):
        return str(self.op_token.lexeme) + " " + str(self.exp)


class Binary(Expression):
    def __init__(self, left_exp, op_token, right_exp):
        if not type(left_exp)  is Expression: raise TypeError("Left expression must be of type Expression")
        if not type(op_token)  is Token:      raise TypeError("Operator token must be of type Token")
        if not type(right_exp) is Expression: raise TypeError("Right expression must be of type Expression")
        self.left_exp = left_exp
        self.op_token = op_token
        self.right_exp = right_exp

    def __str__(self):
        return str(self.left_exp) + " " + self.op_token.lexeme + " " + str(self.right_exp)

