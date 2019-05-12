class Interpreter:

    def __init__(self):
        self.print_buffer = []
        self.identifiers = {}

    def interpret_vardec(self, nodes, line):
        ident = nodes[0].content
        if ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' has already been declared ; line " + line)
        self.identifiers[ident] = self.interpret_expression(nodes[2], line)   

    def interpret_expression(self, exp, line):
        if    exp.node_type == "LITERAL_EXP": return self.interpret_literal_exp(exp, line)
        elif  exp.node_type == "BINARY_EXP" : return self.interpret_binary_exp(exp, line)
        elif  exp.node_type == "STRING_EXP" : return '"' + exp.children[1].content + '"'
        raise Exception("Unexpected Expression type ; line " + line)
    
    def interpret_literal_exp(self, exp, line):
        literal = exp.children[0]
        if literal.node_type == "LITERAL":
            return int(literal.content) if literal.content.isdigit() else float(literal.content)
        elif literal.node_type == "IDENTIFIER" and literal.content in self.identifiers.keys():
            return self.identifiers[literal.content]
        raise Exception("Identifier '" + literal.content + "' referenced before declaration ; line " + line)

    def interpret_binary_exp(self, exp, line):
        left = self.interpret_expression(exp.children[0], line)
        op = exp.children[1].content
        right = self.interpret_expression(exp.children[2], line)
        if op == "+":
            return left + right

    def interpret_line(self, line_tree):
        line = line_tree.line
        nodes = line_tree.children
        for i in range(len(nodes)):
            if nodes[i].node_type == "VAR-DEC": 
                self.interpret_vardec(nodes[i+1:], line)

    def interpret(self, parse_tree):
        for subtree in parse_tree.children:
            print("\nInterpreting line " + subtree.line)
            self.interpret_line(subtree)
        #return self.print_buffer
        return self.identifiers