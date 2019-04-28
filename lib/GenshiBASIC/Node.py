from Token import Token

class Node:

    def __init__(self, node_type=None, content=None, line=None, children=None):
        self.node_type = '' if node_type is None else node_type
        self.content = '' if content is None else content
        self.line = -1 if line is None else line
        self.children = [] if children is None else children

    def get_nodes(self):
        return self.children

    def len_children(self):
        return len(self.children)

    def is_empty(self):
        return self.node_type=='' and self.content=='' and self.line==-1 and len(self.children)==0

    def add_child(self, child, as_token=False):
        if as_token:
            child = Node(child.token_type, child.lexeme, child.line, [])
        self.children.append(child)

    def add_children(self, other):
        for o in other:
            self.add_child(o)

    def __str__(self):
        s = "type: " + self.node_type.ljust(20) + "content: " + str(self.content).ljust(10)
        s += "    line: " + str(self.line)
        s += "    children: Node[" + str(len(self.children)) + "]" + "\n"
        for child in self.children:
            s += child.__str__()
        return s

