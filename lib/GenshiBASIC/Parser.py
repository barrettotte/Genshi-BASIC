from collections import OrderedDict
from Expression import *
from Node import Node
from Stack import Stack
from Token import Token
import Constants as constants
import Utils as utils

class Parser:

    def __init__(self):
        self.node_tree = Node("ROOT")
        self.parse_tree = Node("PROGRAM", line=-1)

    def print_node_stack(self, node_stack):
        print("+------STACK-------+")
        for i in reversed(node_stack.as_list()): 
            print("|   " + str(i.node_type).ljust(15) + "|")
        print("+------------------+")

    def node_from_token(self, token):
        tok_type = token.token_type
        if token.token_type == "LITERAL" and token.literal == "IDENTIFIER":
            tok_type = "IDENTIFIER"
        return Node(tok_type, token.lexeme, token.line, [])

    def node_tree_to_lines(self, node_tree):
        lines = OrderedDict()
        for n in node_tree.children:
            if not n.node_type in ["FOR-START", "FOR-END", "FOR-DEF"] :
                line_num = n.line
                if not line_num in lines: 
                    lines[line_num] = []
                lines[line_num].append(n)
        return lines

    def parse_expression_node(self, node_stack, line):
        if node_stack.peek().node_type == "BINARY_EXP":
            return self.parse_binary_expression(node_stack, line)
        elif node_stack.peek().node_type == "UNARY_EXP":
            return self.parse_unary_expression(node_stack, line)
        elif node_stack.peek().node_type == "GROUPING_EXP":
            exp = node_stack.pop()
            if not node_stack.is_empty():
                if node_stack.peek().node_type == "BINARY":
                    return self.parse_binary_operator(exp, node_stack, line)
                elif node_stack.peek().node_type == "RIGHT_PAREN":
                    return exp
                return self.parse_expression(node_stack, line)
            raise Exception("Unexpected end of Expression on line " + line)
        raise Exception("Unexpected Token " + node_stack.peek().node_type)

    def parse_grouping_expression(self, node_stack, line):
        if node_stack.is_empty():
            raise Exception("Unterminated grouping expression. Expected missing ')' on line " + line)
        left = node_stack.pop()
        exp = self.parse_expression(node_stack, line)
        if not node_stack.is_empty():
            if node_stack.peek().node_type == "RIGHT_PAREN":
                right = node_stack.pop()
                return Expression_Node(Grouping_Exp(left, exp, right), line=line)
        raise Exception("Unterminated grouping expression. Expected missing ')' on line " + line)

    def parse_binary_expression(self, node_stack, line):
        left = node_stack.pop()
        if node_stack.peek().node_type == "BINARY":
            return self.parse_binary_operator(left, node_stack, line)
        elif node_stack.peek().node_type == "RIGHT_PAREN":
            return left
        raise Exception("Unexpected Token " + node_stack.peek().node_type)
    
    def parse_binary_operator(self, left, node_stack, line):
        op = node_stack.pop()
        if not node_stack.is_empty():
            if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
                node_stack.push(Expression_Node(Literal_Exp(node_stack.pop()), line=line))
            if node_stack.peek().node_type == "LEFT_PAREN":
                right = self.parse_grouping_expression(node_stack, line)
            elif node_stack.peek().node_type == "UNARY":
                right = self.parse_unary_operator(node_stack.pop(), node_stack, line)
            else:
                right = node_stack.pop()
            exp = Expression_Node(Binary_Exp(left, op, right), line=line)
            if not node_stack.is_empty():
                node_stack.push(exp)
                return self.parse_expression(node_stack, line)
            return exp
        raise Exception("Unexpected end of Binary expression on line " + line)

    def parse_unary_expression(self, node_stack, line):
        left = node_stack.pop()
        if node_stack.peek().node_type == "BINARY":
            return self.parse_binary_operator(left, node_stack, line)
        elif node_stack.peek().node_type == "RIGHT_PAREN":
            return left
        raise Exception("Unexpected Token " + node_stack.peek().node_type)

    def parse_unary_operator(self, left, node_stack, line):
        if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
            node_stack.push(Expression_Node(Literal_Exp(node_stack.pop()), line=line))
        right = node_stack.pop()
        if right.node_type == "LEFT_PAREN":
            node_stack.push(right)
            right = self.parse_grouping_expression(node_stack, line)
        exp = Expression_Node(Unary_Exp(left, right), line=line)
        if not node_stack.is_empty():
            node_stack.push(exp)
            return self.parse_expression(node_stack, line)
        return exp

    def parse_expression(self, node_stack, line):
        while not node_stack.is_empty():
            # Very convenient debug here... #
            #print("Parsing an Expression...")
            #print("    " + node_stack.peek().node_type)
            #self.print_node_stack(node_stack)
            
            if type(node_stack.peek()) is Expression_Node:
                return self.parse_expression_node(node_stack, line)
            elif node_stack.peek().node_type == "LEFT_PAREN":
                group = self.parse_grouping_expression(node_stack, line)
                if node_stack.is_empty():
                    return group
                node_stack.push(group)
                return self.parse_expression(node_stack, line)
            elif node_stack.peek().node_type == "UNARY":
                left = node_stack.pop()
                if not node_stack.is_empty():
                    return self.parse_unary_operator(left, node_stack, line)
                raise Exception("Unexpected end of unary expression on line " + line)
            elif node_stack.peek().node_type == "BINARY":
                left = node_stack.pop()
                if not node_stack.is_empty():
                    return self.parse_binary_operator(left, node_stack, line)
                raise Exception("Unexpected end of binary expression on line " + line)
            elif node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
                literal = Expression_Node(Literal_Exp(node_stack.pop()), line=line)
                if node_stack.peek().node_type == "BINARY":
                    return self.parse_binary_operator(literal, node_stack, line)
                elif node_stack.peek().node_type == "RIGHT_PAREN":
                    return literal
                raise Exception("Unexpected Token " + node_stack.peek().node_type)
            raise Exception("Unexpected Token " + node_stack.peek().node_type) 
        raise Exception("Unexpected parsing failure")

    def syntax_err(self, expected, line, statement, context=""):
        stmt = self.statement_str(statement)
        stmt_len = len("SyntaxError: " + stmt)
        msg = "Expected " + expected
        if context != "": msg += " for " + context
        msg += " on line " + line
        raise SyntaxError(stmt + "\n" + (" "*stmt_len) + "^^^^^\n  " + msg + "\n")

    def parse_parameters(self, node_stack, line, statement):
        param_nodes = []
        while not node_stack.is_empty() and node_stack.peek().node_type != "RIGHT_PAREN":
            if node_stack.peek().node_type == "IDENTIFIER":
                param_nodes.append(node_stack.pop())
                if node_stack.peek().node_type == "IDENTIFIER":
                    self.syntax_err("','", line, statement, context="Function declaration")
            elif node_stack.peek().node_type == "COMMA":
                param_nodes.append(node_stack.pop())
                if node_stack.peek().node_type == "COMMA":
                    self.syntax_err("identifier", line, statement, context="Function declaration")
            else:
                self.syntax_err("',' or identifier", line, statement, context="Function declaration")
        return param_nodes

    def make_parse_tree(self, node_tree):
        grammar_rules = constants.GRAMMAR_RULES
        self.parse_tree = Node("PROGRAM", line=-1)
        node_stack = Stack(Node())
        lines = self.node_tree_to_lines(node_tree)
        for line, nodes in lines.items():
            node_stack.push_list(reversed(nodes))
            statement = Node("STATEMENT", line=line)
            while not node_stack.is_empty():
                rule = grammar_rules[node_stack.peek().node_type]
                statement.add_child(node_stack.pop())
                for elem in rule:
                    if elem == node_stack.peek().node_type:
                        statement.add_child(node_stack.pop())
                    elif elem == "PARAMETERS":
                        statement.add_children(self.parse_parameters(node_stack, line, statement))
                    elif elem == "EXPRESSION":
                        statement.add_child(self.parse_expression(node_stack, line))
                    else:
                        self.syntax_err(elem, line, statement, context="Function declaration")
            #print(statement)
            self.parse_tree.add_child(statement)
        #print(self.parse_tree)
        return self.parse_tree
            
    def make_node_tree(self, tokens, root):
        node_stack = Stack(Node())
        index = len(tokens)-1
        nest_lvl = 0
        while index >= 0:
            token = tokens[index]
            if token.token_type == "FOR-START":
                nest_lvl -= 1
                for_node = self.node_from_token(token)
                while not node_stack.is_empty():
                    for_node.add_child(node_stack.pop())
                    if node_stack.peek().node_type == "FOR-END":
                        break
                node_stack.push(for_node)
            elif token.token_type != "COMMENT":
                node_stack.push(self.node_from_token(token))
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
        return self.parse_tree