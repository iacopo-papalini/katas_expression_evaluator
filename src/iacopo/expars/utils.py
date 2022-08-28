from collections import deque


#  https://stackoverflow.com/a/59903465/349620
class PeekIterator:
    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.peeked = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self.peeked:
            return self.peeked.popleft()
        return next(self.iterator)

    def peek(self, ahead=0):
        while len(self.peeked) <= ahead:
            self.peeked.append(next(self.iterator))
        return self.peeked[ahead]

    def has_next(self):
        try:
            self.peek()
            return True
        except StopIteration:
            return False
