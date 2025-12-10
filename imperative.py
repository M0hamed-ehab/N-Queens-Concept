
from classes.board import Board
########################################################--Imperative--#########################################################

# Concept: Higher-order function
def attempt_place(board, row, col, on_safe_callback):
    if board.is_safe(row, col):
        return on_safe_callback(row, col)
    return False


def backtrack_imperative(board, col=0):
    if col >= board.N:
        return True

    for row in range(board.N):
        # use higher-order function 
        def place_and_continue(r, c):
            board.place_queen(r, c)
            if backtrack_imperative(board, c + 1):
                return True
            board.remove_queen(r, c)
            return False
        if attempt_place(board, row, col, place_and_continue):
            return True

    return False

###########################################################################################################################