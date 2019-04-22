from GenshiBASIC.Node import Node
from GenshiBASIC.Stack import Stack
from GenshiBASIC.Token import Token
import GenshiBASIC.Utils as utils

class Parser:

    def __init__(self):
        self.node_tree = Node("ROOT")
        self.parse_tree = Node()

    def node_from_token(self, token, level=None):
        return Node(token.token_type, token.lexeme, token.line, [], level)

    def make_parse_tree(self, node_tree):
        node_stack = Stack(Node())
        parse_tree = Node()
        for n in node_tree.children:
            if not n.node_type in ["FOR-START", "FOR-END", "FOR-DEF"] :
               print(n) 
               # TODO: Left off here!
            
    def make_node_tree(self, tokens, root):
        node_stack = Stack(Node())
        index = len(tokens)-1
        nest_lvl = 0
        while index >= 0:
            token = tokens[index]
            if token.token_type == "FOR-START":
                nest_lvl -= 1
                for_node = self.node_from_token(token, level=nest_lvl)
                while node_stack.count() > 0:
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
        while node_stack.count() > 0:
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