from GenshiBASIC.Node import Node
from GenshiBASIC.Stack import Stack
import GenshiBASIC.Utils as utils

class Parser:

    def __init__(self):
        print("Made Parser") # TODO: Remove this

    def node_from_token(self, token, level=None):
        return Node(token.token_type, token.lexeme, token.line, [], level)

    def make_tree(self, tokens, root):
        token_stack = Stack()
        for i in range(len(tokens)):
            node = Node()
            if tokens[i].token_type == "FOR-START":
                node = self.node_from_token(tokens[i])
            if not node.is_empty():
                root.add_child(node)
        return root

    def parse(self, tokens):
        flattened = []
        for line_num, token_list in tokens.items():
            for t in token_list:
                flattened.append(t)
        for token in flattened:
            print(str(token))
        root = Node("ROOT")
        tree = self.make_tree(flattened, root)
        return tree