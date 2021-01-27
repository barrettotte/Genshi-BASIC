# stack data structure
# Pretty much a wrapper over a list with some more utility functions

class Stack:

    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def push_all(self, item_list):
        for item in item_list:
            self.push(item)

    def pop(self):
        if len(self.__items) == 0:
            raise Exception('Cannot pop item from empty stack')
        return self.__items.pop()

    def peek(self):
        if len(self.__items) == 0:
            raise Exception('Cannot peek item from empty stack')
        return self.__items[len(self.__items) - 1]

    def clear(self):
        self.__items.clear()

    def as_list(self):
        return self.__items

    def __str__(self):
        s = f'stack: {len(self.__items)} item(s)\n'
        for item in self.__items:
            s += f'  - {str(item)}\n'
        return s

    def __len__(self):
        return len(self.__items)
