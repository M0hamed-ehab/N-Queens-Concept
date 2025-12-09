#########################################################--Functional--########################################################



def copy_row(board,ri,ci=0):
    if ci == len(board[ri]):
        return ()
    return (board[ri][ci],) + copy_row(board, ri, ci + 1)

def copy_rest(row, i=0):
    if i >= len(row):
        return ()
    return (row[i],) + copy_rest(row, i+1)


def is_safe_row(board, row, col, i=0):
    if i == col:
        return True
    if board[row][i] == 1:
        return False
    return is_safe_row(board, row, col, i + 1)


def is_safe_upper(board, row, col):
    def check(i, j):
        if i < 0 or j < 0:
            return True
        if board[i][j]== 1:
            return False
        return check(i - 1, j - 1)
    return check(row, col)


def is_safe_lower(board, row, col):
    n = len(board)

    def check(i, j):
        if i >= n or j < 0:
            return True
        if board[i][j] == 1:
            return False
        return check(i + 1, j - 1)
    return check(row, col)


def is_safe_functional(board, row, col):
    return (
        is_safe_row(board, row, col) and
        is_safe_upper(board, row, col) and
        is_safe_lower(board, row, col)
    )

def copy_board(board, i=0):
    if i == len(board):
        return ()
    return (copy_row(board,i),) + copy_board(board, i + 1)

def try_rows(board, col, row=0):
    n = len(board)
    if row == n:
        return None, False

    if is_safe_functional(board, row, col):
        # new_board = copy_board(board)
        # new_board[row][col] = 1
        new_board = set_cell(board, row, col, 1)
        result, found = backtrack_functional(new_board, col + 1)
        if found:
            return result, True

    return try_rows(board, col, row + 1)


def set_cell(board, row, col, value):
    def replace_row(list,i,new):
        if i==0:
            return (new,)+copy_rest(list,1)
        return (list[0],)+replace_row(copy_rest(list,1),i-1,new)
    
    
    def replace(row,i):
        if i==0:
            newrow=replace_row(row[0],col,value)
            return (newrow,)+copy_rest(row,1)
        return (row[0],)+replace(copy_rest(row,1),i-1)
    return replace(board,row)

def backtrack_functional(board, col=0):
    n = len(board)
    if col >= n:
        return board, True

    return try_rows(board, col)