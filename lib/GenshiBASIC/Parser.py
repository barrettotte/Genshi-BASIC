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

    def print_node_stack(self, node_stack, label=""):
        header = "------" + label + "STACK-------"
        print("+" + header + "+")
        for i in reversed(node_stack.as_list()): 
            print("|   " + str(i.node_type).ljust(15+len(label)) + "|")
        print("+" + "-"*len(header) + "+")

    def node_from_token(self, token):
        tok_type = token.token_type
        if token.token_type == "LITERAL" and token.literal == "IDENTIFIER":
            tok_type = "IDENTIFIER"
        return Node(tok_type, token.lexeme, token.line, [])

    def node_tree_to_lines(self, node_tree):
        lines = OrderedDict()
        for n in node_tree.children:
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
                if node_stack.is_empty():
                    return literal
                elif node_stack.peek().node_type == "BINARY":
                    return self.parse_binary_operator(literal, node_stack, line)
                elif node_stack.peek().node_type in ["RIGHT_PAREN", "FOR-TO", "FOR-STEP"]:
                    return literal
                raise Exception("Unexpected Token " + node_stack.peek().node_type)
            raise Exception("Unexpected Token " + node_stack.peek().node_type) 
        raise Exception("Unexpected parsing failure")

    def statement_str(self, statement):
        s = statement.line
        for n in statement.children:
            s += " " + n.str_statement() if isinstance(n, Expression_Node) else " " + str(n.content)
        return s

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
                if not node_stack.is_empty and node_stack.peek().node_type != "COMMA":
                    self.syntax_err("','", line, statement, context="Parameters definition")
            elif node_stack.peek().node_type == "COMMA":
                param_nodes.append(node_stack.pop())
                if not node_stack.is_empty and node_stack.peek().node_type != "IDENTIFIER":
                    self.syntax_err("identifier", line, statement, context="Parameters definition")
            else:
                self.syntax_err("',' or identifier", line, statement, context="Parameters definition")
        return param_nodes

    def parse_arguments(self, node_stack, line, statement):
        arg_nodes = []
        arg_stack = Stack()
        if not node_stack.peek().node_type == "LEFT_PAREN":
            self.syntax_err("'('", line, statement, context="Arguments definition")
        arg_nodes.append(node_stack.pop())
        
        while not node_stack.is_empty():
            if node_stack.peek().node_type == "COMMA":
                arg_nodes.append(node_stack.pop())
            elif not node_stack.peek().node_type in ["LEFT_PAREN", "UNARY", "LITERAL", "IDENTIFIER"]:
                self.syntax_err("Expression", line, statement, context="Arguments definition")
            while not node_stack.is_empty() and node_stack.peek().node_type != "COMMA":
                arg_stack.push(node_stack.pop())
            arg_stack = utils.flip_stack(arg_stack)

            if not arg_stack.is_empty():
                if arg_stack.peek().node_type == "RIGHT_PAREN":
                    self.syntax_err("Expression", line, statement, context="Arguments definition")
                arg_nodes.append(self.parse_expression(arg_stack, line))
                if not arg_stack.is_empty() and arg_stack.peek().node_type == "RIGHT_PAREN":
                    arg_nodes.append(arg_stack.pop())
        if arg_nodes[-1].node_type != "RIGHT_PAREN":
            self.syntax_err("')'", line, statement, context="Arguments definition")
        return arg_nodes

    def parse_statement(self, node_stack, line):
        grammar_rules = constants.GRAMMAR_RULES
        statement = Node("STATEMENT", line=line)
        while not node_stack.is_empty():
            rule = grammar_rules[node_stack.peek().node_type]
            statement.add_child(node_stack.pop())
            for elem in rule:
                if node_stack.is_empty():
                    raise SyntaxError("Unexpected end of statement on line " + line)
                elif elem == node_stack.peek().node_type:
                    statement.add_child(node_stack.pop())
                elif elem == "PARAMETERS":
                    statement.add_children(self.parse_parameters(node_stack, line, statement))
                elif elem == "ARGUMENTS":
                    statement.add_children(self.parse_arguments(node_stack, line, statement))
                elif elem == "EXPRESSION":
                    statement.add_child(self.parse_expression(node_stack, line))
                else:
                    raise SyntaxError("Expected element [" + elem + "] on line " + line)
            if len(rule) == 0 and not node_stack.is_empty():
                raise SyntaxError("Unexpected element [" + node_stack.pop().node_type + "] on line " + line)
        return statement

    def make_parse_tree(self, node_tree):
        node_stack = Stack(Node())
        tree = Node("PROGRAM", line=-1)
        for line, nodes in self.node_tree_to_lines(node_tree).items():
            node_stack.push_list(reversed(nodes))
            tree.add_child(self.parse_statement(node_stack, line))
            
        return tree
    
    # This was kind of leftover from a different train of thought, everything works now, 
    #   but it seems a little silly to transform to a tree, a stack, and back to a tree. 
    #   Should definitely refactor if you still have enough sanity left at the end.
    def make_node_tree(self, tokens, root):
        node_stack = Stack(Node())
        index = len(tokens)-1
        nest_lvl = 0
        while index >= 0:
            token = tokens[index]
            nest_lvl -= 1 if (token.token_type == "FOR-DEF") else 0
            nest_lvl += 1 if (token.token_type == "FOR-END") else 0
            if token.token_type != "COMMENT":
                node_stack.push(self.node_from_token(token))
            index -= 1
        if nest_lvl != 0: raise SyntaxError("Missing 'ENDFOR' statement")
        while not node_stack.is_empty():
            root.add_child(node_stack.pop())
        return root

    def parse(self, tokens):
        tokens_flat = []
        for line_num, token_list in tokens.items():
            for t in token_list:
                tokens_flat.append(t)
        self.node_tree = self.make_node_tree(tokens_flat, Node("ROOT"))
        self.parse_tree = self.make_parse_tree(self.node_tree)
        return self.parse_tree