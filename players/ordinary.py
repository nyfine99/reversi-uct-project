"""
In this file, we implement ordinary UCT. More details will be given further on.
"""

# performing necessary imports
from reversi import *
import supervisor
import random
import time
import math

# a global variable which tracks the set of all sets seen;
# this is split into "X" and "O" to prevent one player from peeking 
# at another's data
ord_seen = {"X": {}, "O": {}} # map from player -> 
# (map from states -> [r_state, t_state])
# states are represented as board strings

ord_total_tries = 0 # tracks how many times the get_move algorithm
# has been run; I wanted to compare this to improved and helped with debugging


def get_board_string(board):
    """
    board: a reversi board
    
    Returns the board's state represented as a string.
    """

    s = ""
    for i in range(0,8):
        for j in range(0,8):
            s = s + board[i][j]
    return s


def get_board_string_after_move(move, curr_tile, board):
    """
    move: the desired move; an open location on the board
    curr_tile: the tile of the player whose turn it currently is to move
    board: a reversi board
    
    Returns the state of the board after move is made by curr_tile,
    represented as a string.
    """

    board_copy = getBoardCopy(board)
    makeMove(board_copy, curr_tile, move[0], move[1])
    s = get_board_string(board_copy)
    return s


def Q_value(r_next_move, t_next_move, t_total, curr_tile):
    """
    r_next_move: r_y, the observed reward at state y, where y is the 
    state of the board after the move being examined is made
    t_next_move: t_y, the number of times we have explored state y, where
    y is the state of the board after the move being examined is made
    t_total: the total explorations we have made of the current state
    curr_tile: the tile of the player whose turn it currently is to move
    
    Returns the "score" for the player owning curr_tile of making the move 
    currently being explored.
    """

    if curr_tile == "X":
        # we are at a max node, so we want to maximize:
        return r_next_move + math.sqrt(2 * math.log(t_total)/t_next_move)
    # we are at a min node, so we want to maximize:
    return 1 - r_next_move + math.sqrt(2 * math.log(t_total)/t_next_move)
    # note: the maximization fo the result is done in UCB_choose

def UCB_choose(board, curr_state, possibleMoves, curr_tile, tile_seen):
    """
    board: a reversi board
    curr_state: the string representation of the board's current state
    (passed in to save time)
    possibleMoves: all possibleMoves that the player whose turn it is
    can currently make
    curr_tile: the tile of the player whose turn it currently is to move
    tile_seen: the set of seen states, mapped to the each state's r and t 
    values
    
    Returns the move which UCB_choose, as described in class, would select
    from the set of possible moves.
    """
    
    random.shuffle(possibleMoves)
    # tracks the sum of t values for all child states; this will be relevant
    # if all child states have already been seen
    t_total = 0
    for i in range(0, len(possibleMoves)):
        # obtaining the child state corresponding to making the move 
        # possibleMoves[i]
        new_state = get_board_string_after_move(
            possibleMoves[i], curr_tile, board)
        if new_state not in tile_seen:
            # this move has not yet been examined, so we return it
            return possibleMoves[i]
        t_total += tile_seen[new_state][1]

    # if this point is reached, all children states have been seen; so, we
    # will find the move with the best "score" as specified in the UCB_choose
    # pseudocode from class; the move which best maximizes exploration vs 
    # exploitation
    curr_max = -1
    best_move = -1
    for i in range(0, len(possibleMoves)):
        new_state = get_board_string_after_move(
            possibleMoves[i], curr_tile, board)
        r_t_pair = tile_seen[new_state] # this has the list [r_y, t_y] 
        # for child state y
        curr_Q_val = Q_value(r_t_pair[0], r_t_pair[1], t_total, curr_tile)
        if curr_Q_val > curr_max:
            # in this case, the possibleMoves[i] has a better score than 
            # the other moves checked so far
            curr_max = curr_Q_val
            best_move = possibleMoves[i]
    
    return best_move


def UCT(board, curr_tile, tile_seen):
    """
    board: a reversi board
    curr_tile: the tile of the player whose turn it currently is to move
    tile_seen: the set of seen states, mapped to the each state's r and t 
    values
    
    Updates tile_seen appropriately for the current board based on the 
    results of the successive calls to UCT.
    Returns the r value of the current move = the r value of the next move
    chosen by UCB_choose (which is then used by the previous calls to 
    recursively update tile_seen).
    """

    # get the current state of the board in string form, so that we can use it
    # as a key in tile_seen
    curr_state = get_board_string(board)
    if curr_state not in tile_seen:
        # in this case, we must initialize the r and t values for the current
        # state; we will have adjusted these values by the end of the run
        tile_seen[curr_state] = [0, 0]

    valid_moves = getValidMoves(board, curr_tile)
    if valid_moves == []:
        # in this case, no one can move, and the game is done
        # we treat X as max nodes and O as min nodes, so return 1 if X wins,
        # 0 if O wins
        scores = getScoreOfBoard(board)
        if scores["X"] > scores["O"]:
            # X wins; adjust r appropriately and return r value
            tile_seen[curr_state][0] = (tile_seen[curr_state][0] * 
                tile_seen[curr_state][1] + 1.0)/(tile_seen[curr_state][1] +1.0)
            # increment t value
            tile_seen[curr_state][1] = tile_seen[curr_state][1] + 1.0
            return 1.0
        elif scores["X"] == scores["O"]:
            # tie; adjust r appropriately and return r value
            tile_seen[curr_state][0] = (tile_seen[curr_state][0] * 
                tile_seen[curr_state][1] + 0.5)/(tile_seen[curr_state][1] +1.0)
            # increment t value
            tile_seen[curr_state][1] = tile_seen[curr_state][1] + 1.0
            return 0.5
        else:
            # O wins; adjust r appropriately and return r value
            tile_seen[curr_state][0] = (tile_seen[curr_state][0] * 
                tile_seen[curr_state][1])/(tile_seen[curr_state][1] +1.0)
            # increment t value
            tile_seen[curr_state][1] = tile_seen[curr_state][1] + 1.0
            return 0.0
    
    # if we have reached this point, there are valid moves to be made
    # we can save time by passing in board and curr_state to UCB_choose
    next_move = UCB_choose(board, curr_state, valid_moves, curr_tile, tile_seen) 
    next_tile = "O"
    if curr_tile == "O":
        next_tile = "X"
    # next tile is now set to the tile of the player whose turn is next
    # we make the move chosen by UCB_choose...
    makeMove(board, curr_tile, next_move[0], next_move[1])
    # ... and then use a recursive call to UCT to find the r value of 
    # that move ...
    val_next_move = UCT(board, next_tile, tile_seen)
    # ... and then update the r and t values of the current move accordingly
    tile_seen[curr_state][0] = (tile_seen[curr_state][0] * 
        tile_seen[curr_state][1] + val_next_move)/(tile_seen[curr_state][1] + 1.0)
    tile_seen[curr_state][1] = tile_seen[curr_state][1] + 1.0

    # and we return the r value for the current move
    return val_next_move

def get_move(board, tile):
    """
    board: a reversi board
    tile: the tile of the player whose turn it is to move
    
    Returns the best known move that can be made after a call to UCT.
    """

    # importing the set of all states seen so far
    global ord_seen
    # importing a counter which counts the total calls to get_move;
    # interesting to see the statistics on this
    global ord_total_tries
    # creating a copy of the board, so that the board is not edited 
    # by our call to UCT
    board_copy = getBoardCopy(board)

    # call UCT
    UCT(board_copy, tile, ord_seen[tile])

    # take the best known move; if X is currently moving, this is the move
    # with the highest r value, and if O is moving, this is the move with
    # the lowest r value
    poss_moves = getValidMoves(board, tile)
    curr_best = [-1, -1]
    if tile =="X":
        curr_max_r = -1
        for move in poss_moves:
            post_move = get_board_string_after_move(move, tile, board)

            if post_move in ord_seen[tile] and (
                ord_seen[tile][post_move][0]) > curr_max_r:
                curr_max_r = ord_seen[tile][post_move][0]
                curr_best = move

    else:
        curr_min_r = 2
        for move in poss_moves:
            post_move = get_board_string_after_move(move, tile, board)

            if post_move in ord_seen[tile] and (
                ord_seen[tile][post_move][0]) < curr_min_r:
                curr_min_r = ord_seen[tile][post_move][0]
                curr_best = move

    ord_total_tries = ord_total_tries + 1
    return curr_best