from reversi import *
from node import *
from Minimax import *
import math
import random
import copy
import numpy as np
class MCTS:
    def __init__(self, board):
        self.board = board

    # def isWinState(self, board, player):
    #     if self.isTerminalState()
    #
    # def isLoseState(self, board, player):
    #

    def isTerminalState(self, board):
        return not (len(self.makeMoves(1, board)) > 0 or len(self.makeMoves(-1, board)) > 0)

    def makeMoves(self, player, board):
        tempGame = ReversiGame()
        tempGame.board = copy.deepcopy(board)
        tempGame.player = player
        movesList = tempGame.get_legal_moves(player)
        arr = []
        if len(movesList) == 0:
            newBoard = copy.deepcopy(board)
            arr.append((None, newBoard))
            return arr
        for move in movesList:
            tempGame.execute_move(move)
            newBoard = copy.deepcopy(tempGame.board)
            tempGame.board = copy.deepcopy(board)
            tempGame.player = player
            arr.append((move, newBoard))
        return arr

    def expand(self, node: Node):
        #self.VNode_count += 1
        (move, newBoard) = node._untried_actions.pop()
        child_node = Node(newBoard, node, move, -node.player)
        # possible_moves = self.makeMoves(playerMove, newMap)
        # child_node._untried_actions = random.shuffle(possible_moves)
        child_node._untried_actions = self.makeMoves(-node.player, newBoard)
        node.children.append(child_node)
        return child_node

    def rollout(self, node: Node):
        Player = node.player
        Board = copy.deepcopy(node.board)
        count = 0
        while (not self.isTerminalState(Board)) and count <= 30:
            possible_moves = self.makeMoves(Player, Board)
            count += 1
            if (len(possible_moves)) == 0:
                break
            (move, newBoard) = random.choice(possible_moves)
            Player = -Player
            Board = newBoard
        if Player == node.player:
            return evaluate(Board, Player)
        else:
            return -evaluate(Board, Player)

    def back_propagate(self, v: Node, node: Node, result):
        while v != node.parent:
            v.N += 1.
            v.Q += result
            v = v.parent

    def best_child(self, node: Node):
        max_value = float('-inf')
        best_child = None
        for child in node.children:
            if child.value() > max_value:
                max_value = child.value()
                best_child = child
                #print(child, child.value())
        return best_child

    def _tree_policy(self, node: Node):
        current_node = node
        while not self.isTerminalState(current_node.board):
            if not current_node.is_fully_expanded():
                return self.expand(current_node)
            else:
                if len(current_node.children) == 0:
                    break
                current_node = self.best_child(current_node)
        return current_node

    def best_action(self, node: Node, simulation_no):

        for i in range(simulation_no):
            v = self._tree_policy(node)
            reward = self.rollout(v)
            self.back_propagate(v, node, reward)

        return self.best_child(node)

    def solve(self, node: Node, simulation_no = 30):
        start_node = node
        #start_node._untried_actions = self.makeMoves(player, self.board)
        selected_node = self.best_action(start_node, simulation_no)
        # self.VNode_count = len(self.expanded)
        # if not self.map.hasWon(selected_node.player):
        #     self.can_find_win_path = False
            # print("Haven't found win path, best path so far is: ")
        #self.winPath = selected_node.makePathTo()
        return selected_node
        # return self.best_child(start_node)