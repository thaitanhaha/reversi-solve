import math
class Node:
    def __init__(self, board: list, parent, move: list, player):
        self.board = board
        self.player = player
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = []
        self._untried_actions = []

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def value(self, c_param=math.sqrt(2)):
        if self.N == 0:
            return float('inf')
        else:
            return self.Q / self.N + c_param * math.sqrt(math.log(self.parent.N) / self.N)
