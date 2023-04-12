from node import *
from reversi import *
score_board = [[99, -8, 8, 6, 6, 8, -8, 99],
               [-8, -24, -4, -3, -3, -4, -24, -8],
               [8, -4, 7, 4, 4, 7, -4, 8],
               [6, -3, 4, 0, 0, 4, -3, 6],
               [6, -3, 4, 0, 0, 4, -3, 6],
               [8, -4, 7, 4, 4, 7, -4, 8],
               [-8, -24, -4, -3, -3, -4, -24, -8],
               [99, -8, 8, 6, 6, 8, -8, 99]
               ]
def minimax(node: Node, maxDepth, alpha, beta):
    if (len(node.children) == 0) or maxDepth == 0:
        return evaluate(node.board, node.player)
    for child in node.children:
        result = minimax(child, maxDepth-1, -beta, -alpha)
        new_val = -result
        if new_val > alpha:
            alpha = new_val
        if alpha >= beta:
            value = alpha
        return value

def evaluate(board, player):
    res = 0
    for i in range(8):
        for j in range(8):
            res += (board[i][j]*score_board[i][j])
    return res*player
