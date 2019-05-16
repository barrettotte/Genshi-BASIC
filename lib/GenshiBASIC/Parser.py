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
        if node_stack.peek().node_type in ["GROUPING_EXP", "BINARY_EXP", "UNARY_EXP", "FUNCTION_EXP"]:
            left = node_stack.pop()
            if not node_stack.is_empty():
                if node_stack.peek().node_type == "BINARY":
                    return self.parse_binary_operator(left, node_stack, line)
                elif node_stack.peek().node_type in ["RIGHT_PAREN", "THEN"]:
                    return left
                raise Exception("Unexpected Token " + node_stack.peek().node_type)
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
    
    def parse_binary_operator(self, left, node_stack, line):
        op = node_stack.pop()
        if not node_stack.is_empty():
            if node_stack.peek().node_type in ["LITERAL", "IDENTIFIER"]:
                right = self.parse_literal_expression(node_stack.pop(), node_stack, line)
            elif node_stack.peek().node_type == "LEFT_PAREN":
                right = self.parse_grouping_expression(node_stack, line)
            elif node_stack.peek().node_type == "UNARY":
                right = self.parse_unary_operator(node_stack.pop(), node_stack, line)
            elif node_stack.peek().node_type in ["ONE-PARAM", "TWO-PARAM", "THREE-PARAM"]:
                right = Expression_Node(Function_Exp(node_stack.pop(), self.parse_arguments(node_stack, line)), line)
            elif node_stack.peek().node_type == "QUOTATION":
                raise SyntaxError("Unexpected start of STRING expression on line " + line)
            else:
                right = node_stack.pop()
            exp = Expression_Node(Binary_Exp(left, op, right), line=line)
            if not node_stack.is_empty():
                node_stack.push(exp)
                return self.parse_expression(node_stack, line)
            return exp
        raise Exception("Unexpected end of Binary expression on line " + line)

    def parse_unary_operator(self, left, node_stack, line):
        if node_stack.peek().node_type in ["LITERAL", "IDENTIFIER"]:
            node_stack.push(self.parse_literal_expression(node_stack.pop(), node_stack, line))
        right = node_stack.pop()
        if right.node_type == "LEFT_PAREN":
            node_stack.push(right)
            right = self.parse_grouping_expression(node_stack, line)
        exp = Expression_Node(Unary_Exp(left, right), line=line)
        if not node_stack.is_empty():
            node_stack.push(exp)
            return self.parse_expression(node_stack, line)
        return exp

    def parse_literal_expression(self, literal, node_stack, line):
        if node_stack.is_empty() or node_stack.peek().node_type == "THEN":
            return Expression_Node(Literal_Exp(literal), line=line)
        elif node_stack.peek().node_type == "BINARY":
            return self.parse_binary_operator(Expression_Node(Literal_Exp(literal), line=line), node_stack, line)
        elif node_stack.peek().node_type in ["RIGHT_PAREN", "FOR-TO", "FOR-STEP"]:
            return Expression_Node(Literal_Exp(literal), line=line)
        elif node_stack.peek().node_type == "LEFT_PAREN":
            func = Expression_Node(Function_Exp(literal, self.parse_arguments(node_stack, line)), line=line)
            if not node_stack.is_empty():
                node_stack.push(func)
                return self.parse_expression(node_stack, line)
            return func
        elif node_stack.peek().node_type in ["EQUALS", "QUOTATION"]:
            return literal
        raise Exception("Unexpected Token " + node_stack.peek().node_type)

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
                literal = node_stack.pop()
                return self.parse_literal_expression(literal, node_stack, line)
            elif node_stack.peek().node_type in ["ONE-PARAM", "TWO-PARAM", "THREE-PARAM"]:
                identifier = node_stack.pop()
                if not node_stack.is_empty():
                    bif = Expression_Node(Function_Exp(identifier, self.parse_arguments(node_stack,line)),line)
                    if not node_stack.is_empty():
                        node_stack.push(bif)
                        return self.parse_expression(node_stack, line)
                    return bif
                raise Exception("Unexpected end of function call on line " + line)
            elif node_stack.peek().node_type in ["GO-DEF", "NO-PARAM", "STRING", "PRINT"]:
                return node_stack.pop()
            elif node_stack.peek().node_type == "QUOTATION":
                return self.parse_string(node_stack, line)
            raise Exception("Unexpected Token " + node_stack.peek().node_type) 
        raise Exception("Unexpected parsing failure")

    def statement_str(self, statement):
        if statement == '':
            return ''
        s = statement.line if statement != '' else ''
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
        return Node("PARAMETERS", line=line, children=param_nodes)

    def parse_arguments(self, node_stack, line, statement=''):
        arg_nodes = []
        arg_stack = Stack()
        if not node_stack.peek().node_type == "LEFT_PAREN":
            self.syntax_err("'('", line, statement, context="Arguments definition")
        arg_nodes.append(node_stack.pop())
        while not node_stack.is_empty():
            if node_stack.peek().node_type == "COMMA":
                arg_nodes.append(node_stack.pop())
            elif not node_stack.peek().node_type in constants.EXPRESSION_START:
                if node_stack.peek().node_type == "RIGHT_PAREN":
                    node_stack.pop()
                    return Node("ARGUMENTS", line=line, children=[])
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
        arg_stack = utils.flip_stack(arg_stack)
        while not arg_stack.is_empty():
            node_stack.push(arg_stack.pop())
        return Node("ARGUMENTS", line=line, children=arg_nodes)

    def parse_string(self, node_stack, line):
        s = []
        if node_stack.peek().node_type == "QUOTATION":
            start = node_stack.pop()
            if not node_stack.is_empty():
                while node_stack.peek().node_type != "QUOTATION":
                    if node_stack.peek().node_type == "STRING":
                        s.append(node_stack.pop())
                    else:
                        raise SyntaxError("Expected STRING literal on line " + line)
                if node_stack.peek().node_type == "QUOTATION":
                    return Node("STRING_EXP", line=line, children=[start]+s+[node_stack.pop()])
            raise SyntaxError("Unexpected end of STRING on line " + line)
        raise SyntaxError("Expected start of STRING on line " + line)

    def parse_statement(self, node_stack, line):
        grammar_rules = constants.GRAMMAR_RULES
        statement = Node("LINE", line=line)
        rule = grammar_rules[node_stack.peek().node_type]
        statement.add_child(node_stack.pop())
        if isinstance(rule, dict):
            rule = rule[node_stack.peek().node_type]
            if node_stack.peek().node_type == "EQUALS":
                statement.add_child(node_stack.pop())
        for elem in rule:
            if node_stack.is_empty():
                raise SyntaxError("Unexpected end of statement on line " + line)
            elif elem == node_stack.peek().node_type:
                statement.add_child(node_stack.pop())
            elif elem == "PARAMETERS":
                statement.add_child(self.parse_parameters(node_stack, line, statement))
            elif elem == "ARGUMENTS":
                args = self.parse_arguments(node_stack, line, statement)
                if statement.children[-1].node_type == "IDENTIFIER":
                    exp = Expression_Node(Function_Exp(statement.children[-1], args), line)
                    statement.children[-1] = exp
                else:
                    statement.add_child(args)
            elif elem == "EXPRESSION":
                statement.add_child(self.parse_expression(node_stack, line))
            elif elem == "STRING":
                if node_stack.peek().node_type in constants.EXPRESSION_START:
                    statement.add_child(self.parse_expression(node_stack, line))
                elif statement.children[-1].node_type == "PRINT":
                    statement.children[-1].add_child(self.parse_string(node_stack, line))
                else:
                    raise SyntaxError("Expected PRINT statement on line " + line)
            else:
                raise SyntaxError("Expected element [" + elem + "] on line " + line)
        if not node_stack.is_empty():
            if node_stack.peek().node_type == "EQUALS":
                statement.add_child(node_stack.pop())
                exp = self.parse_expression(node_stack, line)
                if not node_stack.is_empty():
                    raise SyntaxError("Parsing failed on line " + line + ". Elements still on stack")
                statement.add_child(exp)
            elif node_stack.peek().node_type in constants.EXPRESSION_START:
                statement.add_child(self.parse_expression(node_stack, line))
            else:
                raise SyntaxError("Parsing failed on line " + line + ". Elements still on stack")
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