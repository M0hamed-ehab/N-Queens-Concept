
from classes.board import Board
########################################################--Imperative--#########################################################

def backtrack_imperative(board, col=0):
    if col >= board.N:
        return True

    for i in range(board.N):
        if board.is_safe(i, col):
            board.place_queen(i, col)

            if backtrack_imperative(board, col + 1):
                return True

            board.remove_queen(i, col)

    return False

###############################################################################################################################