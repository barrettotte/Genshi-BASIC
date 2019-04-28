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

    def print_node_stack(self, node_stack):
        for i in node_stack.as_list():
            print(i.node_type)
        print("--------------------")


    def parse_expression_node(self, node_stack, line):
        if node_stack.peek().node_type == "BINARY_EXP":
            return self.parse_binary_expression(node_stack, line)
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
        if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
            node_stack.push(Expression_Node(Literal_Exp(node_stack.pop()), line=line))
        if node_stack.peek().node_type in ["BINARY_EXP", "LITERAL_EXP"]:
            left = node_stack.pop()
            if node_stack.peek().node_type == "BINARY":
                return self.parse_binary_operator(left, node_stack, line)
            elif node_stack.peek().node_type == "RIGHT_PAREN": 
                return left
            raise Exception("Unexpected Token " + node_stack.peek().node_type)
        raise Exception("Unexpected Token " + node_stack.peek().node_type)
    
    def parse_binary_operator(self, left, node_stack, line):
        op = node_stack.pop()
        if not node_stack.is_empty():
            if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
                node_stack.push(Expression_Node(Literal_Exp(node_stack.pop()), line=line))
            if node_stack.peek().node_type == "LEFT_PAREN":
                right = self.parse_grouping_expression(node_stack, line)
            else:
                right = node_stack.pop()
            exp = Expression_Node(Binary_Exp(left, op, right), line=line)
            if not node_stack.is_empty():
                node_stack.push(exp)
                return self.parse_expression(node_stack, line)
            return exp
        raise Exception("Unexpected end of Binary expression on line " + line)

    def parse_expression(self, node_stack, line):
        while not node_stack.is_empty():
            print("Parsing an Expression...")
            print("    " + node_stack.peek().node_type)
            self.print_node_stack(node_stack)
            
            if type(node_stack.peek()) is Expression_Node:
                print("^^XXXXXXXXXX")
                return self.parse_expression_node(node_stack, line)
            elif node_stack.peek().node_type == "LEFT_PAREN":
                group = self.parse_grouping_expression(node_stack, line)
                if node_stack.is_empty():
                    return group
                node_stack.push(group)
                return self.parse_expression(node_stack, line)
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

    def statement_str(self, statement):
        s = statement.line
        for n in statement.children:
            s += " " + n.str_statement() if isinstance(n, Expression_Node) else str(n.content)
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
            statement = Node("STATEMENT", line=line)
            for i in reversed(range(len(nodes))):
                node_stack.push(nodes[i])

            # TODO: REFACTOR THIS MONSTER
            # TODO: This can probably be done with a list
            while not node_stack.is_empty():
                if node_stack.peek().node_type == "FUNC-DEF":
                    statement.add_child(node_stack.pop())
                    if node_stack.peek().node_type == "FUNCTION":
                        statement.add_child(node_stack.pop())
                        if node_stack.peek().node_type == "IDENTIFIER":
                            statement.add_child(node_stack.pop())
                            if node_stack.peek().node_type == "LEFT_PAREN":


                                # TODO: Parse 'parameters' function
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
                                # END 'parameters'


                                if node_stack.peek().node_type == "EQUALS":
                                    statement.add_child(node_stack.pop())
                                    exp = self.parse_expression(node_stack, line)
                                    if isinstance(exp, Expression):
                                        exp = Expression_Node(exp, line=line)
                                    elif exp is None:
                                        raise Exception("Expression was evaluated to NoneType")
                                    statement.add_child(exp)
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
                    break
            print("\n-------------------")
            print(statement)

        
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

        return self.node_tree #TODO: Change to parse_tree when finished