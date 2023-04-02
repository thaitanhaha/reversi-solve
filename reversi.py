import numpy as np
from enum import Enum
import copy

SEARCH_DEPTH = 10000

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
        flips = (flip for direction in DIRECTION
                 for flip in self.get_flips(pos, DIRECTION[direction]))

        for x, y in flips:
            self.board[x][y] = self.player

        self.player = -self.player

    def make_temp_move(self, temp_board, pos, curr_check_player):
        flips = (flip for direction in DIRECTION
                 for flip in self.get_flips(pos, DIRECTION[direction]))
        for x, y in flips:
            temp_board[x][y] = self.player

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
    
    def minimax(self, temp_board, depth, curr_check_player = player):
        '''
        Implements the minimax algorithm with alpha-beta pruning to determine the best move
        for the given player on the given board.
        '''
        if depth == 0 or self.get_winner():
            return self.count(curr_check_player)

        if curr_check_player == 1:
            best_score = float('-inf')
            for move in self.get_legal_moves(curr_check_player):
                new_board = self.make_temp_move(temp_board, (move[0], move[1]), curr_check_player)
                score = self.minimax(new_board, depth - 1, -curr_check_player)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_legal_moves(curr_check_player):
                new_board = self.make_temp_move(temp_board, (move[0], move[1]), curr_check_player)
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
        for move in self.get_legal_moves(curr_check_player):
            new_board = self.make_temp_move(temp_board, (move[0], move[1]), curr_check_player)
            score = self.minimax(new_board, SEARCH_DEPTH, -curr_check_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move


if __name__ == "__main__":
    a = ReversiGame()
    a.display() 
    
    while (True):
        temp = a.get_legal_moves(a.player)
        # print("Player", a.player, "has legal moves", temp)
        if temp != None:
            x, y = temp[-1]
        else:
            i = input()
        print("Player play", x, y)
        # x, y = [int(x) for x in input().split()]
        # while ((x,y) not in temp):
        #     x, y = [int(x) for x in input().split()]    
        a.execute_move((x,y))
        a.display()

        # temp = a.get_legal_moves(a.player)
        # print("Player", a.player, "has legal moves", temp)
        temp_board = copy.deepcopy(a.board)
        temp_player = a.player
        x, y = a.get_best_move(temp_board, temp_player)
        print("Computer play", x, y)
        # x, y = [int(x) for x in input().split()]
        # while ((x,y) not in temp):
        #     x, y = [int(x) for x in input().split()]    
        a.execute_move((x,y))
        a.display()