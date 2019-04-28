class Stack:

    def __init__(self, T=None, items=None):
        self.T = None if T is None else type(T)
        self.items = [] if items is None else items

    def get_type(self):
        return self.T

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        if self.T is None or isinstance(item, self.T):
            self.items.append(item)
        else:
            raise TypeError(
              "This stack is of type " + str(self.T) + " . Cannot add item of type " + str(type(item))
            )

    def pop(self):
        if self.is_empty(): raise Exception("Cannot pop an empty stack")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty(): raise Exception("Cannot peek an empty stack")
        return self.items[len(self.items)-1]

    def count(self):
        return len(self.items)
    
    def clear(self):
        self.items.clear()

    def as_list(self):
        return self.items

    def copy(self):
        return self(self.T, self.items.copy())

    def __str__(self):
        return "Stack" + str(self.T) + " of size " + str(self.count())

    def contains(self, attribute, val):
        try:
            for i in self.items:
                x = getattr(i, attribute)
                if val == x:
                    return True
        except: 
            raise Exception(str(self.T) + " has no attribute " + attribute)
        return False
        