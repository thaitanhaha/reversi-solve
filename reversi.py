import numpy as np
from enum import Enum
import copy
import random
import time

SEARCH_DEPTH = 3

LOOP = 1
win = 0
lose = 0

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
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self):
        self.player = 1
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]
        
    def display(self):
        print("   0  1  2  3  4  5  6  7")
        for i in range(8):
            print(i, end = "")
            for j in range(8):
                if self.board[i][j] == 1:
                    print("  1", end = "")
                elif self.board[i][j] == -1:
                    print(" -1", end = "")
                else:
                    print("  0", end = "")
            print("")

    def count(self, curr_board = None, curr_check_player = None):
        '''
        Count to check win state
        '''
        if curr_board is None:
            curr_board = self.board
        if curr_check_player is None:
            curr_check_player = self.player
        count = 0
        for x in range(8):
            for y in range(8):
                if curr_board[x][y] == curr_check_player:
                    count += 1
        return count
    
    def get_winner(self, curr_board = board) -> GAMESTATE:
        '''
        Check if the game is end or not. If yes, who win?
        '''
        if len(self.get_legal_moves(curr_board, 1)) > 0:
            return GAMESTATE.Running
        if len(self.get_legal_moves(curr_board, -1)) > 0:
            return GAMESTATE.Running

        player1_count = self.count(curr_board, 1)
        player2_count = self.count(curr_board, -1)
        if player1_count == player2_count:
            return GAMESTATE.Draw
        elif player1_count > player2_count:
            return GAMESTATE.Player1
        else:
            return GAMESTATE.Player2
    
    def get_positions(self, curr_board = None, needed_player = None) -> list:
        '''
        Get all position on the board that equal to needed_player (default = current player) 
        '''
        if curr_board is None:
            curr_board = self.board
        
        if needed_player is None:
            needed_player = self.player

        positions = []
        for y in range(8):
            for x in range(8):
                if curr_board[x][y] == needed_player:
                    positions.append((x, y))
        return positions
    
    def get_legal_moves(self, curr_board = board, needed_player = player) -> list:
        '''
        Get all moves for each position that collected from get_positions()
        '''
        moves = set()
        for position in self.get_positions(curr_board, needed_player):
            newmoves = self.get_moves_for_position(curr_board, position)
            moves.update(newmoves)
        return list(moves)
    
    def get_moves_for_position(self, curr_board = None, position = (0,0)):
        '''
        Get all moves for a position
        '''
        if curr_board is None:
            curr_board = self.board

        (x,y) = position
        temp_player = curr_board[x][y]
        if temp_player == 0:
            return None

        moves = []
        for dir in DIRECTION:
            move = self.discover_move(curr_board, position, DIRECTION[dir])
            if move:
                moves.append(move)
        return moves
    
    def discover_move(self, curr_board = board, origin_pos = (0,0), dir = (1,1)):
        '''
        Traverse 8 directions to check moves for a position
        '''
        x, y = origin_pos
        temp_player = curr_board[x][y]
        flips = []

        for x, y in self.increment_move(origin_pos, dir):
            if curr_board[x][y] == 0:
                if flips:
                    return x, y
                else:
                    return None
            elif curr_board[x][y] == temp_player:
                return None
            elif curr_board[x][y] == -temp_player:
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
        flips = (flip for direction in DIRECTION
                 for flip in self.get_flips(self.board, pos, DIRECTION[direction], self.player))

        for x, y in flips:
            self.board[x][y] = self.player

        self.player = -self.player

    def make_temp_move(self, temp_board = None, pos = (0,0), curr_check_player = None):
        if temp_board is None:
            temp_board = self.board
        flips = (flip for direction in DIRECTION
                 for flip in self.get_flips(temp_board, pos, DIRECTION[direction], curr_check_player))
        for x, y in flips:
            temp_board[x][y] = curr_check_player
        return temp_board

    def get_flips(self, curr_board = None, origin = (0,0), direction = (1,1), needed_player = None):
        '''
        Flip all of the unit from origin position to the direction
        '''
        if curr_board is None:
            curr_board = self.board
        if needed_player is None:
            needed_player = self.player

        flips = [origin]

        for x, y in self.increment_move(origin, direction):
            if curr_board[x][y] == 0:
                return []
            elif curr_board[x][y] == -needed_player:
                flips.append((x, y))
            elif curr_board[x][y] == needed_player:
                return flips

        return []
    
    def lost_turn(self):
        self.player = -self.player
    
    def minimax(self, temp_board, depth, curr_check_player = player):
        '''
        Implements the minimax algorithm with alpha-beta pruning to determine the best move
        for the given player on the given board.
        '''
        temp = self.get_winner(temp_board)
        if temp == GAMESTATE.Player1 or temp == GAMESTATE.Draw:
            return -1000
        elif temp == GAMESTATE.Player2:
            return 1000
        temp = self.get_legal_moves(temp_board, -1)
        if temp == []:
            return -1000
        temp = self.get_legal_moves(temp_board, 1)
        if temp == []:
            return 1000
        if depth == 0:
            return self.count(temp_board, -1) - self.count(temp_board, 1)

        if curr_check_player == -1:
            best_score = float('-inf')
            temp = self.get_legal_moves(temp_board, curr_check_player)
            for move in temp:
                temp_temp_board = [[i for i in row] for row in temp_board]
                new_board = self.make_temp_move(temp_temp_board, (move[0], move[1]), curr_check_player)
                score = self.minimax(new_board, depth - 1, -curr_check_player)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            temp = self.get_legal_moves(temp_board, curr_check_player)
            for move in temp:
                temp_temp_board = [[i for i in row] for row in temp_board]
                new_board = self.make_temp_move(temp_temp_board, (move[0], move[1]), curr_check_player)
                score = self.minimax(new_board, depth - 1, -curr_check_player)
                best_score = min(best_score, score)
            return best_score


    def get_best_move(self, temp_board, curr_check_player):
        """
        Returns the best move for the given player on the given board using the minimax algorithm
        with alpha-beta pruning.
        """
        best_move = None
        best_score = float('-inf')
        temp = self.get_legal_moves(temp_board, curr_check_player)
        for move in temp:
            temp_temp_board = [[i for i in row] for row in temp_board]
            new_board = self.make_temp_move(temp_temp_board, (move[0], move[1]), curr_check_player)
            score = self.minimax(new_board, SEARCH_DEPTH, -curr_check_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move


def two_player(a : ReversiGame):
    while (True):
        temp = a.get_legal_moves(a.board, a.player)
        print("Player", a.player, "has legal moves", temp)
        x, y = [int(x) for x in input().split()]
        while ((x,y) not in temp):
            x, y = [int(x) for x in input().split()]    
        a.execute_move((x,y))
        a.display()

def random_player_vs_computer(a : ReversiGame):
    global win
    global lose
    while True:
        temp = a.get_legal_moves(a.board, a.player)
        if temp != []:
            x, y = temp[random.randint(0, len(temp)-1)]
            print("Random play", x, y)
            a.execute_move((x,y))
        else:
            if a.get_winner(a.board) != GAMESTATE.Running:
                # print("END GAME")
                res = a.count(a.board, -1) - a.count(a.board, 1)
                if res > 0:
                    win += 1
                else: 
                    lose += 1
                print(res, end = " ")
                break
            else:
                a.lost_turn()
        a.display()

        temp_board = [[i for i in row] for row in a.board]
        temp = a.get_best_move(temp_board, -1)
        if temp is not None:
            x, y = temp
            print("Computer play", x, y)
            a.execute_move((x,y))
        else:
            if a.get_winner(a.board) != GAMESTATE.Running:
                # print("END GAME")
                res = a.count(a.board, -1) - a.count(a.board, 1)
                if res > 0:
                    win += 1
                else: 
                    lose += 1
                print(res, end = " ")
                break
            else:
                a.lost_turn()
        a.display()

if __name__ == "__main__":
    for i in range (LOOP):
        a = ReversiGame()
        time_start = time.time()
        # a.display() 
        random_player_vs_computer(a)
        time_end = time.time()
        print(time_end - time_start)
        a = None
    
    print()
    print(win, lose)