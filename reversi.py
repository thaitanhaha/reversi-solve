import numpy as np
from node import *
from enum import Enum
from MCTS import *

DIRECTION = {
    "up-left": (-1, -1), 
    "up-right": (1, -1),
    "up": (0, -1),
    "down-left": (-1, 1), 
    "down-right": (1, 1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

class GAMESTATE(Enum):
    Running = 0,
    Player1 = 1,
    Player2 = -1,
    Draw = 2,

class ReversiGame():
    player = 1
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, -1, 1, 0, 0, 0],
                      [0, 0, 0, 1, -1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        
    def display(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    print("  1", end = "")
                elif self.board[i][j] == -1:
                    print(" -1", end = "")
                else:
                    print("  0", end = "")
            print("")

    def count(self, needed_player = player):
        '''
        Count to check win state
        '''
        count = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == needed_player:
                    count += 1
        return count
    
    def get_winner(self) -> GAMESTATE:
        '''
        Check if the game is end or not. If yes, who win?
        '''
        if len(self.get_legal_moves(1)) > 0 or len(self.get_legal_moves(-1)) > 0:
            return GAMESTATE.Running

        player1_count = self.count(1)
        player2_count = self.count(-1)
        if player1_count == player2_count:
            return GAMESTATE.Draw
        elif player1_count > player2_count:
            return GAMESTATE.Player1
        else:
            return GAMESTATE.Player2
    
    def get_positions(self, needed_player = player) -> list:
        '''
        Get all position on the board that equal to needed_player (default = current player) 
        '''
        positions = []
        for y in range(8):
            for x in range(8):
                if self.board[x][y] == needed_player:
                    positions.append((x, y))
        return positions
    
    def get_legal_moves(self, needed_player = player) -> list:
        '''
        Get all moves for each position that collected from get_positions()
        '''
        moves = set()
        for position in self.get_positions(needed_player):
            newmoves = self.get_moves_for_position(position)
            moves.update(newmoves)
        return list(moves)
    
    def get_moves_for_position(self, position):
        '''
        Get all moves for a position
        '''
        (x,y) = position
        temp_player = self.board[x][y]
        if temp_player == 0:
            return None

        moves = []
        for dir in DIRECTION:
            move = self.discover_move(position, DIRECTION[dir])
            if move:
                moves.append(move)
        return moves
    
    def discover_move(self, origin_pos, dir):
        '''
        Traverse 8 directions to check moves for a position
        '''
        x, y = origin_pos
        temp_player = self.board[x][y]
        flips = []

        for x, y in self.increment_move(origin_pos, dir):
            if self.board[x][y] == 0:
                if flips:
                    return x, y
                else:
                    return None
            elif self.board[x][y] == temp_player:
                return None
            elif self.board[x][y] == -temp_player:
                flips.append((x, y))

    def increment_move(self, move, direction):
        '''
        Traverse
        '''
        move = list(map(sum, zip(move, direction)))
        while all(map(lambda x: 0 <= x < 8, move)):
            yield move
            move = list(map(sum, zip(move, direction)))

    def execute_move(self, pos):
        '''
        Do the move at the pos position
        '''
        if not pos:
            self.player = -self.player
            return
        flips = (flip for direction in DIRECTION
                 for flip in self.get_flips(pos, DIRECTION[direction]))

        for x, y in flips:
            self.board[x][y] = self.player

        self.player = -self.player


    def get_flips(self, origin, direction):
        '''
        Flip all of the unit from origin position to the direction
        '''
        flips = [origin]

        for x, y in self.increment_move(origin, direction):
            if self.board[x][y] == 0:
                return []
            elif self.board[x][y] == -self.player:
                flips.append((x, y))
            elif self.board[x][y] == self.player:
                return flips

        return []

if __name__ == "__main__":
    a = ReversiGame()
    a.display()

    mcts = MCTS(a.board)
    curr_node = Node(a.board, None, None, a.player)
    curr_node._untried_actions = mcts.makeMoves(a.player, a.board)
    while not curr_node.is_fully_expanded():
        mcts.expand(curr_node)

    print(str(curr_node.move), len(curr_node.children))
    for child in curr_node.children:
        print(str(child.move), end = ", ")
    while (True):
        # temp = a.get_legal_moves(a.player)
        # print("Player", a.player, "has legal moves", temp)
        # x, y = [int(x) for x in input().split()]
        # while ((x, y) not in temp):
        #     x, y = [int(x) for x in input().split()]
        # for child in curr_node.children:
        #     if child.move == (x, y):
        #         curr_node = child
        #         break
        # a.execute_move((x, y))
        # a.display()
        # print(str(curr_node.move), len(curr_node.children))
        # #if len(curr_node.children) == 0:
        # if len(curr_node._untried_actions) == 0 and len(curr_node.children) == 0:
        #     curr_node._untried_actions = mcts.makeMoves(curr_node.player, curr_node.board)
        # while not curr_node.is_fully_expanded():
        #         mcts.expand(curr_node)
        # print(str(curr_node.move), len(curr_node.children))
        # for child in curr_node.children:
        #     print(str(child.move), end=",")

        temp = a.get_legal_moves(a.player)
        print("Player", a.player, "has legal moves", temp)
        # if len(temp) == 0:
        #     continue
        selected_node = mcts.solve(curr_node)
        selected_move = selected_node.move
        a.execute_move(selected_move)
        a.display()
        curr_node = selected_node
        print(str(curr_node.move), len(curr_node.children))
        # if len(curr_node.children) == 0:
        if len(curr_node._untried_actions) == 0 and len(curr_node.children) == 0:
            curr_node._untried_actions = mcts.makeMoves(curr_node.player, curr_node.board)
        while not curr_node.is_fully_expanded():
            mcts.expand(curr_node)
        print(str(curr_node.move), len(curr_node.children))
        for child in curr_node.children:
            print(str(child.move), end=",")

        # temp = a.get_legal_moves(a.player)
        # print("Player", a.player, "has legal moves", temp)
        # x, y = [int(x) for x in input().split()]
        # while ((x,y) not in temp):
        #     x, y = [int(x) for x in input().split()]
        # a.execute_move((x,y))
        # a.display()

        # temp = a.get_legal_moves(a.player)
        # print("Player", a.player, "has legal moves", temp)
        # selected_node = mcts.solve(curr_node)
        # selected_move = selected_node.move
        # a.execute_move(selected_move)
        # a.display()
        # curr_node = selected_node
        # print(str(curr_node.move), len(curr_node.children))
        # #if len(curr_node.children) == 0:
        # if len(curr_node._untried_actions) == 0 and len(curr_node.children) == 0:
        #     curr_node._untried_actions = mcts.makeMoves(curr_node.player, curr_node.board)
        # while not curr_node.is_fully_expanded():
        #     mcts.expand(curr_node)
        # print(str(curr_node.move), len(curr_node.children))
        # for child in curr_node.children:
        #     print(str(child.move), end=",")

