from GenshiBASIC.Token import Token

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
            child = Node(child.token_type, child.lexeme, child.line, [], self.level)
        self.children.append(child)

    def add_children(self, other):
        self.children += other

    def __str__(self):
        s = { 
            "type": self.node_type,
            "content": self.content,
            "line": self.line,
            "children": "Node[" + str(len(self.children)) + "]",
            "level": self.level
        }
        return str(s)

    def __str__(self, level=0):
        s = "  " * (self.level+1) + "type: " + self.node_type.ljust(15) + "content: " + self.content.ljust(5)
        s += "      level: " + str(self.level) + "    line: " + str(self.line)
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

