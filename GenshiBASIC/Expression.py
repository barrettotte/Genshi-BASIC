from GenshiBASIC.Token import Token


class Expression:
    def __init__(self): pass
    def __str__(self): return ""


class Literal(Expression):
    def __init__(self, val):
        if not isinstance(val, (int, float, str)): 
            raise TypeError("Value of literal can only be of type string, float, or string")
        self.val = val
    
    def __str__(self):
        return str(val)


class Grouping(Expression):
    def __init__(self, exp):
        if not type(exp) is Expression: raise TypeError("Expression must be of type Expression")
        self.exp = exp

    def __str__(self):
        return "(" + str(self.exp) + ")"


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

