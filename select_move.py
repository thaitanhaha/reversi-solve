from reversi import *
from node import *
from MCTS import *

curr_node = None
mcts = None

def select_move(cur_state, player_to_move, remain_time):
    global curr_node, mcts
    if remain_time == 60:
        mcts = MCTS(cur_state)
        curr_node = Node(cur_state, None, None, player_to_move)
    else:
        for child in curr_node.children:
            if child.board == cur_state:
                curr_node = child
                break
    if len(curr_node._untried_actions) == 0 and len(curr_node.children) == 0:
        curr_node._untried_actions = mcts.makeMoves(curr_node.player, curr_node.board)
    while not curr_node.is_fully_expanded():
        mcts.expand(curr_node)
    selected_node = mcts.solve(curr_node)
    selected_move = selected_node.move
    #a.execute_move(selected_move)
    #a.display()
    curr_node = selected_node
    if len(curr_node._untried_actions) == 0 and len(curr_node.children) == 0:
        curr_node._untried_actions = mcts.makeMoves(curr_node.player, curr_node.board)
    while not curr_node.is_fully_expanded():
        mcts.expand(curr_node)
    return selected_move