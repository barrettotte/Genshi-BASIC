from Node import Node


class Expression():
    def __init__(self):  pass
    def __str__(self):   pass
    def get_nodes(self): pass



class Expression_Node(Node):

    def __init__(self, expression, line):
        if not isinstance(expression, Expression):
            raise TypeError("Expression must inherit from Expression")
        nodes = expression.get_nodes()
        return super().__init__(
            node_type=str(expression.__class__.__name__).upper(), 
            content=expression, 
            line=line, 
            children=nodes
        )

    def str_statement(self):
        s = ""
        for n in self.children:
            if isinstance(n, Expression_Node):
                x = "type: " + str(n.node_type).ljust(20) + "content:     "
                x += "line: " + str(self.line) + "   children: Node[" + str(len(self.children)) + "]\n"
                s += x + "\n" + str(n.str_statement())
            else:
                s += str(n)
        return s
    
    def __str__(self):
        s = "type: " + self.node_type.ljust(20) + "content:     "
        s += "line: " + str(self.line) + "    children: Node[" + str(len(self.children)) + "]\n"
        s += self.str_statement()
        return s



class Literal_Exp(Expression):

    def __init__(self, literal_node):
        if not type(literal_node) is Node: 
            raise TypeError("Literal node must be of type Node")
        self.content = literal_node
    
    def __str__(self): 
        return str(self.content)

    def get_nodes(self): 
        return [self.content]



class Grouping_Exp(Expression):

    def __init__(self, left_paren, exp, right_paren):
        if not type(left_paren) is Node:    
            raise TypeError("Left paren must be of type Node")
        if not isinstance(exp, (Expression, Expression_Node)): 
            raise TypeError("Expression must inherit from Expression or Expression_Node")
        if not type(right_paren) is Node:   
            raise TypeError("Right paren must be of type Node")

        self.left_paren = left_paren
        self.exp = exp
        self.right_paren = right_paren

    def __str__(self): 
        return "( " + str(self.exp) + " )"

    def get_nodes(self): 
        return [self.left_paren, self.exp, self.right_paren]



class Unary_Exp(Expression):

    def __init__(self, op_node, exp):
        if not type(op_node) is Node:        
            raise TypeError("Operator node must be of type Node")
        if not isinstance(exp, (Expression, Expression_Node)):  
            raise TypeError("Expression must inherit from Expression or Expression_Node")

        self.op_node = op_node
        self.exp = exp

    def __str__(self): 
        return str(self.op_node.content) + " " + str(self.exp)

    def get_nodes(self): 
        return [self.op_node, self.exp]



class Binary_Exp(Expression):

    def __init__(self, left_exp, op_node, right_exp):
        if not isinstance(left_exp, (Expression, Expression_Node)):
            raise TypeError("Left expression must inherit from Expression or Expression_Node")
        if not type(op_node) is Node:             
            raise TypeError("Node token must be of type Node")
        if not isinstance(right_exp, (Expression, Expression_Node)):
            raise TypeError("Right expression must inherit from Expression or Expression_Node")

        self.left_exp = left_exp
        self.op_node = op_node
        self.right_exp = right_exp

    def __str__(self):
        return str(self.left_exp) + " " + str(self.op_node) + " " + str(self.right_exp)

    def get_nodes(self):
        return [self.left_exp, self.op_node, self.right_exp]

