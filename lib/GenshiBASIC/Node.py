from Token import Token

class Node:

    def __init__(self, node_type=None, content=None, line=None, children=None, level=None):
        self.node_type = '' if node_type is None else node_type
        self.content = '' if content is None else content
        self.line = -1 if line is None else line
        self.children = [] if children is None else children
        self.level = -1 if level is None else level

    def len_children(self):
        return len(children)

    def is_empty(self):
        return self.node_type=='' and self.content=='' and self.line==-1 and len(self.children)==0

    def add_child(self, child, as_token=False):
        if as_token:
            child = Node(child.token_type, child.lexeme, child.line, [], self.level+1)
        child.level += 1
        self.children.append(child)

    def add_children(self, other):
        for o in other:
            self.add_child(o)

    def __str__(self, level=0):
        s = "  " * (self.level+1) + "type: " + self.node_type.ljust(20) + "content: " + str(self.content).ljust(10)
        s += "      level: " + str(self.level).ljust(10) + "    line: " + str(self.line)
        s += " children: Node[" + str(len(self.children)) + "]" + "\n"
        for child in self.children:
            s += child.__str__(self.level+2)
        return s

    def children_str(self, children):
        if self.level >= 0:
            s += "   children: ["
            for child in self.children:
                s += child.node_type + " "
            s += " ]\n"

    def __repr__(self):
        return str(self)