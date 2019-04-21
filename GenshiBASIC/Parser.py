from GenshiBASIC.Node import Node
from GenshiBASIC.Stack import Stack
from GenshiBASIC.Token import Token
import GenshiBASIC.Utils as utils

class Parser:

    def __init__(self):
        self.parse_tree = Node("ROOT")

    def node_from_token(self, token, level=None):
        return Node(token.token_type, token.lexeme, token.line, [], level)

    def make_tree(self, tokens, root):
        node_stack = Stack(Node())
        index = 0
        nest_lvl = 0
        while index < len(tokens):
            token = tokens[index]
            if token.token_type == "FOR-END":
                for_node = self.node_from_token(token, level=nest_lvl-1)
                while node_stack.count() > 0:
                    for_node.add_child(node_stack.pop())
                    if node_stack.peek().node_type == "FOR-START":
                        nest_lvl += 1
                        break
                node_stack.push(for_node)
                nest_lvl -= 1
            else:
                if node_stack.contains("node_type", "IF-DEF"):
                    print("MEME!!!!!!")
                node_stack.push(self.node_from_token(token, level=nest_lvl))
                if token.token_type == "FOR-START": nest_lvl += 1
            index += 1
        for n in node_stack.as_list():
            root.add_child(n)
        return root

    def parse(self, tokens):
        flattened = []
        for line_num, token_list in tokens.items():
            for t in token_list:
                flattened.append(t)
        for token in flattened:
            print(str(token))
        self.parse_tree = Node("ROOT")
        tree = self.make_tree(flattened, self.parse_tree)
        return tree