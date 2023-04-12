from reversi import *
import math
import random
import copy
import numpy as np
class Node:
    def __init__(self, parent, move, player):
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

class MCTS:
    def __init__(self, game: ReversiGame):
        self.game = game
