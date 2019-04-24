from collections import OrderedDict
from GenshiBASIC.Expression import Expression, Binary_Exp, Grouping_Exp, Unary_Exp, Literal_Exp
from GenshiBASIC.Node import Node
from GenshiBASIC.Stack import Stack
from GenshiBASIC.Token import Token
import GenshiBASIC.Utils as utils

class Parser:

    def __init__(self):
        self.node_tree = Node("ROOT")
        self.parse_tree = Node()

    def node_from_token(self, token, level=None):
        tok_type = token.token_type
        if token.token_type == "LITERAL" and token.literal == "IDENTIFIER":
            tok_type = "IDENTIFIER"
        return Node(tok_type, token.lexeme, token.line, [], level)

    def node_tree_to_lines(self, node_tree):
        lines = OrderedDict()
        for n in node_tree.children:
            if not n.node_type in ["FOR-START", "FOR-END", "FOR-DEF"] :
                line_num = n.line
                if not line_num in lines: 
                    lines[line_num] = []
                lines[line_num].append(n)
        return lines

    def parse_expression(self, node_stack, line):
        print("DEBUG Parsing Expression for line " + line) # TODO: DEBUG
        while not node_stack.is_empty():
            if node_stack.peek().node_type == "IDENTIFIER":
                left = Literal_Exp(node_stack.pop())
                if node_stack.peek().node_type == "BINARY":
                    op = node_stack.pop()
                    if node_stack.peek().node_type == "IDENTIFIER" or node_stack.peek().node_type == "LITERAL":
                        right = Literal_Exp(node_stack.pop())
                        if node_stack.is_empty():
                            return Binary_Exp(left, op, right)
                        else:
                            raise SyntaxError("Expected end of expression on line " + line)
            else:
                print("DEBUG break parse_expression()") # TODO: DEBUG
                break

    def make_parse_tree(self, node_tree):
        parse_tree = Node()
        node_stack = Stack(Node())
        statement = Node("STATEMENT", level=0)
        lines = self.node_tree_to_lines(node_tree)

        for line, nodes in lines.items():
            for i in reversed(range(len(nodes))):
                node_stack.push(nodes[i])
            while not node_stack.is_empty():
                if node_stack.peek().node_type == "FUNC-DEF":
                    statement.add_child(node_stack.pop())
                    if node_stack.peek().node_type == "FUNCTION":
                        statement.add_child(node_stack.pop())
                        if node_stack.peek().node_type == "IDENTIFIER":
                            statement.add_child(node_stack.pop())
                            if node_stack.peek().node_type == "LEFT_PAREN":
                                statement.add_child(node_stack.pop())
                                while not node_stack.is_empty() and node_stack.peek().node_type != "RIGHT_PAREN":
                                    if node_stack.peek().node_type == "IDENTIFIER":
                                        statement.add_child(node_stack.pop())
                                    else:
                                        raise SyntaxError("Expected ',' or identifier on line " + line)
                                if node_stack.peek().node_type != "RIGHT_PAREN":
                                    raise SyntaxError("Expected ')' for Function declaration on line " + line)
                                statement.add_child(node_stack.pop())
                                if node_stack.peek().node_type == "EQUALS":
                                    statement.add_child(node_stack.pop())
                                    expression = self.parse_expression(node_stack, line)
                                    statement.add_child(expression)
                                else:
                                    raise SyntaxError("Expected '=' for Function declaration on line " + line)
                            else:
                                raise SyntaxError("Expected '(' for Function declaration on line " + line)
                        else:
                            raise SyntaxError("Expected identifier for Function declaration on line " + line)
                    else:
                        raise SyntaxError("Expected 'FN' for Function declaration on line " + line)

                else:
                    print("DEBUG break make_parse_tree()") # TODO: DEBUG
            print("DEBUG break make_parse_tree() only line 1 for now!") # TODO: DEBUG
        print(statement)
        
    def make_node_tree(self, tokens, root):
        node_stack = Stack(Node())
        index = len(tokens)-1
        nest_lvl = 0
        while index >= 0:
            token = tokens[index]
            if token.token_type == "FOR-START":
                nest_lvl -= 1
                for_node = self.node_from_token(token, level=nest_lvl)
                while not node_stack.is_empty():
                    for_node.add_child(node_stack.pop())
                    if node_stack.peek().node_type == "FOR-END":
                        break
                node_stack.push(for_node)
            elif token.token_type != "COMMENT":
                node_stack.push(self.node_from_token(token, level=nest_lvl))
                if token.token_type == "FOR-END":  nest_lvl += 1
            index -= 1
        if nest_lvl != 0: 
            raise SyntaxError("Missing 'ENDFOR' statement")
        while not node_stack.is_empty():
            root.add_child(node_stack.pop())
        self.node_tree = root
        return self.node_tree

    def parse(self, tokens):
        tokens_flat = []
        for line_num, token_list in tokens.items():
            for t in token_list:
                tokens_flat.append(t)
        self.make_node_tree(tokens_flat, Node("ROOT"))
        self.make_parse_tree(self.node_tree)

        return self.node_tree #TODO: Change to parse_tree when finished