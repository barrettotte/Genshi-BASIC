from collections import OrderedDict
from Expression import *
from Node import Node
from Stack import Stack
from Token import Token
import Utils as utils

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
        print("!!!!!!!!!!!")
        while not node_stack.is_empty():
            # ---- BINARY EXPRESSION ---- #
            if node_stack.peek().node_type == "IDENTIFIER":
                left = Literal_Exp(node_stack.pop())
                if node_stack.peek().node_type == "BINARY":
                    op = node_stack.pop()
                    if node_stack.peek().node_type == "IDENTIFIER" or node_stack.peek().node_type == "LITERAL":
                        right = Literal_Exp(node_stack.pop())
                        print("!!!")
                        print(node_stack.as_list())
                        if node_stack.is_empty():
                            return Binary_Exp(left, op, right)
                        else:
                            raise SyntaxError("Expected end of expression on line " + line)
            # ---- GROUPING EXPRESSION ---- #
            # ---- UNARY EXPRESSION ---- #
            # ---- LITERAL EXPRESSION ---- #
            else:
                print("DEBUG break parse_expression()") # TODO: DEBUG
                break

    def statement_str(self, statement):
        s = statement.line + " "
        for n in statement.children:
            s += str(n.content) + " "
        return s

    def syntax_err(self, expected, line, statement, context=""):
        stmt = self.statement_str(statement)
        stmt_len = len("SyntaxError: " + stmt)
        msg = "Expected " + expected
        if context != "": msg += " for " + context
        msg += " on line " + line
        raise SyntaxError(stmt + "\n" + (" "*stmt_len) + "^^^^^\n  " + msg + "\n")

    def make_parse_tree(self, node_tree):
        parse_tree = Node()
        node_stack = Stack(Node())
        
        lines = self.node_tree_to_lines(node_tree)

        for line, nodes in lines.items():
            statement = Node("STATEMENT", line=line, level=0)
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
                                exp = self.parse_expression(node_stack, line)
                                statement.add_child(node_stack.pop())
                                while not node_stack.is_empty() and node_stack.peek().node_type != "RIGHT_PAREN":
                                    if node_stack.peek().node_type == "IDENTIFIER":
                                        statement.add_child(node_stack.pop())
                                        if node_stack.peek().node_type == "IDENTIFIER":
                                            self.syntax_err("','", line, statement, context="Function declaration")
                                    elif node_stack.peek().node_type == "COMMA":
                                        statement.add_child(node_stack.pop())
                                        if node_stack.peek().node_type == "COMMA":
                                            self.syntax_err("identifier", line, statement, context="Function declaration")
                                    else:
                                        self.syntax_err("',' or identifier", line, statement, context="Function declaration")
                                if node_stack.peek().node_type != "RIGHT_PAREN":
                                    self.syntax_err("')'", line, statement, context="Function declaration")
                                statement.add_child(node_stack.pop())
                                if node_stack.peek().node_type == "EQUALS":
                                    statement.add_child(node_stack.pop())
                                    exp = self.parse_expression(node_stack, line)
                                    statement.add_child(Expression_Node(exp, line=line))
                                else:
                                    self.syntax_err("'='", line, statement, context="Function declaration")
                            else:
                                self.syntax_err("'('", line, statement, context="Function declaration")
                        else:
                            self.syntax_err("identifier", line, statement, context="Function declaration")
                    else:
                        self.syntax_err("'FN'", line, statement, context="Function declaration")
                else:
                    print("DEBUG break make_parse_tree()") # TODO: DEBUG
            print("\n")
            print(statement)
            print(self.statement_str(statement))
        
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