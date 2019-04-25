from GenshiBASIC.Node import Node


class Expression():
    def __init__(self):  raise Exception("Objects deriving from Expression must implement __init__()")
    def __str__(self):   raise Exception("Objects deriving from Expression must implement __str__()")
    def get_nodes(self): raise Exception("Objects deriving from Expression must implement get_nodes()")


class Expression_Node(Node):
    def __init__(self, expression, line, level=0):
        if not issubclass(type(expression), Expression): raise TypeError("Expression must inherit from Expression")
        nodes = expression.get_nodes()
        for n in nodes: n.level+=1
        return super().__init__(
            node_type=str(expression.__class__.__name__).upper(), 
            content=expression, 
            line=line, 
            children=nodes, 
            level=level
        )


class Literal_Exp(Expression):
    def __init__(self, literal_node):
        if not type(literal_node) is Node: raise TypeError("Literal node must be of type Node")
        self.val = literal_node
    
    def __str__(self): return str(self.val.content)
    def get_nodes(self): return [self.val]


class Grouping_Exp(Expression):
    def __init__(self, left_paren, exp, right_paren):
        if not type(left_paren) is Node:  raise TypeError("Left paren must be of type Node")
        if not type(exp) is Expression:   raise TypeError("Expression must be of type Expression")
        if not type(right_paren) is Node: raise TypeError("Right paren must be of type Node")
        self.left_paren = left_paren
        self.exp = exp
        self.right_paren = right_paren

    def __str__(self): return "( " + str(self.exp) + " )"
    def get_nodes(self): return [self.left_paren] + self.exp.get_nodes() + [self.right_paren]


class Unary_Exp(Expression):
    def __init__(self, op_node, exp):
        if not type(op_node)  is Node: raise TypeError("Operator node must be of type Node")
        if not type(exp) is Expression:  raise TypeError("Expression must be of type Expression")
        self.op_node = op_node
        self.exp = exp

    def __str__(self): return str(self.op_node.content) + " " + str(self.exp)
    def get_nodes(self): return [self.op_node] + self.exp.get_nodes()


class Binary_Exp(Expression):
    def __init__(self, left_exp, op_node, right_exp):
        if not isinstance(left_exp, Expression):  raise TypeError("Left expression must be of type Expression")
        if not type(op_node)   is Node:           raise TypeError("Node token must be of type Node")
        if not isinstance(right_exp, Expression): raise TypeError("Right expression must be of type Expression")
        self.left_exp = left_exp
        self.op_node = op_node
        self.right_exp = right_exp

    def __str__(self): return str(self.left_exp) + " " + self.op_node.content + " " + str(self.right_exp)
    def get_nodes(self): return self.left_exp.get_nodes() + [self.op_node] + self.right_exp.get_nodes()

