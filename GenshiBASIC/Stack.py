class Stack:

    def __init__(self, items=None):
        self.items = [] if items is None else items

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.is_empty() else self.items.pop()
    
    def peek(self):
        return None if self.is_empty() else self.items[len(self.items)-1]

    def size(self):
        return len(self.items)