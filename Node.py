class Node:
    def __init__(self, id, isLast, needRollback, type):
        self.id = id
        self.isLast = isLast
        self.needRollback = needRollback
        self.type = type

    def __lt__(self, other):
        return self.id < other.id
