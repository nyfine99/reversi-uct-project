from reversi import *
import supervisor
import random
import time

def get_move(board, tile):
	possibleMoves = getValidMoves(board, tile)
	random.shuffle(possibleMoves)
	#print(timeout_limit)
	return possibleMoves[0]

