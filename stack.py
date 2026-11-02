class StackEmptyError(Exception):
    pass

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("Stack kosong")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise StackEmptyError("Stack kosong")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items.clear()

    def to_list(self):
        return list(reversed(self.items))

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(reversed(self.items))