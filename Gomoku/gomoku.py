def is_empty(board): # Done :D
    '''Return True iff there are no stones on the board
    '''
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != ' ':
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x): # Done :D
    '''Return "OPEN" when the sequence is open, "SEMIOPEN" when the
    sequence is semi-open, and "CLOSED" when the sequence is closed

    Analyzes the sequence of length length that ends at
    location (y_end, x_end)

    Assume that the sequence is complete (ie. you are not given a
    subsequence) and valid, and contains stones of only one colour

    (d_y, d_x) are directions: ie...
        (0,1) is left to right
        (1,0) is bottom to top
        (1,1) is up right diagonal
        (1,-1) is down left diagonal
    '''
    # finding direction
    if d_y == 0 and d_x == 1:
        direction = "left to right"        # ends at right
    if d_y == 1 and d_x == 0:
        direction = "top to bottom"        # ends at bottom
    if d_y == 1 and d_x == 1:
        direction = "up left to low right" # ends lower right
    if d_y == 1 and d_x == -1:
        direction = "up right to low left" # ends top right

    # Number of bounded sides
    bounded_sides = 0

    if direction == "top to bottom":
    # checking top
        # checking for board edge
        if x_end + 1 - length == 0:
            bounded_sides += 1
        # if not against board edge checking for open spot
        if x_end + 1 - length != 0:
            if board[x_end - length][y_end] != ' ':
                bounded_sides += 1
    # checking bottom
        # checking for board edge
        if x_end + 1 == len(board):
            bounded_sides += 1
        # if not against board edge checking for open spot
        if x_end + 1 != len(board):
            if board[x_end + 1][y_end] != ' ':
                bounded_sides += 1

    if direction == "left to right":
    # checking right side
        # checking for board edge
        if y_end + 1 == len(board):
            bounded_sides += 1
        # if not against right side
        if y_end + 1 != len(board):
            if board[x_end][y_end + 1] != ' ':
                bounded_sides += 1
    # checking left side
        # checking for board edge
        if y_end + 1 - length == 0:
            bounded_sides += 1
        # if not against left edge checking for open spot
        if y_end + 1 - length != 0:
            if board[x_end][y_end - length] != ' ':
                bounded_sides += 1

    if direction == "up left to low right":
    # checking top left
        # checking for edge
        if x_end + 1 - length == 0 or y_end + 1 - length == 0:
            bounded_sides += 1
        # if not at edge check for open spot
        if x_end + 1 - length != 0 and y_end + 1 - length != 0:
            if board[x_end - length][y_end - length] != ' ':
                bounded_sides += 1
    # checking bottom right
        # checking for edge
        if x_end + 1 == len(board) or y_end + 1 == len(board):
            bounded_sides += 1
        if x_end + 1 != len(board) and y_end + 1 != len(board):
            if board[x_end + 1][y_end + 1] != ' ':
                bounded_sides += 1

    if direction == "up right to low left":
    # checking bottom left
        # checking for board edge
        if x_end + 1 == len(board) or y_end == 0:
            bounded_sides += 1
        # if not against the edge checking for open spot
        if x_end + 1 != len(board) and y_end != 0:
            if board[x_end + 1][y_end -1] != ' ':
                bounded_sides += 1
    # checking top right
        # checking for board edge
        if x_end + 1 - length == 0 or y_end + length == len(board):
            bounded_sides += 1
        # if not against edge checking for open space
        if x_end + 1 - length != 0 and y_end + length != len(board):
            if board[x_end - length][y_end + length] != ' ':
                bounded_sides += 1

    # determining openness
    if bounded_sides == 0:
        return "OPEN"
    if bounded_sides == 1:
        return "SEMIOPEN"
    if bounded_sides == 2:
        return "CLOSED"

# if __name__ == '__main__':
#     board = make_empty_board(8)
#     board[3][3] = "w"
#     board[2][4] = "w"
#     board[1][5] = "w"
#     board[0][6] = "b"
#     print_board(board)
#     y_end = 2
#     x_end = 7
#     length = 3
#     d_y = 1
#     d_x = -1
#     print(is_bounded(board, y_end, x_end, length, d_y, d_x))

def detect_row(board, col, y_start, x_start, length, d_y, d_x): # Done :D
    '''Analyze row (R) of squares that starts at location
    (y_start,x_start) and goes in direction (d_y,d_x).

    Return a tuple whose first element is the number of open
    sequences of colour col of length length in the row R, and
    whose second element is the number of semi-open sequences of
    colour col of length length in the row R

    Assume (y_start,x_start) is on edge of the board and only
    complete sequences count

    Assume length is an int >= 2
    '''
    # direction:
    if d_y == 0 and d_x == 1:
        direction = "left to right"        # ends at right
    if d_y == 1 and d_x == 0:
        direction = "top to bottom"        # ends at bottom
    if d_y == 1 and d_x == 1:
        direction = "up left to low right" # ends lower right
    if d_y == 1 and d_x == -1:
        direction = "up right to low left" # ends top right

    # Creating list of individual sequences

    sequence_list = []
    res = []

    if direction == "top to bottom":
        for i in range(len(board) - x_start):
            x_cord = x_start + i
            y_cord = y_start
            if board[x_cord][y_cord] == col:
                res.append([x_cord, y_cord])
            if board[x_cord][y_cord] != col or x_cord == len(board) - 1:
                if len(res) == length:
                # only want to look at sequences of length length
                    sequence_list.append(res)
                    res = []
                if len(res) != length:
                    res = []

    if direction == "left to right":
        for i in range(len(board) - y_start):
            x_cord = x_start
            y_cord = y_start + i
            if board[x_cord][y_cord] == col:
                res.append([x_cord, y_cord])
            if board[x_cord][y_cord] != col or y_cord == len(board) - 1:
                if len(res) == length:
                # only want to look at sequences of length length
                    sequence_list.append(res)
                    res = []
                if len(res) != length:
                    res = []

    if direction == "up left to low right":
        if y_start > x_start:
            for i in range(len(board) - y_start):
                x_cord = x_start + i
                y_cord = y_start + i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or y_cord == len(board) - 1:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []
        if x_start > y_start:
            for i in range(len(board) - x_start):
                x_cord = x_start + i
                y_cord = y_start + i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or x_cord == len(board) - 1:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []
        if x_start == y_start:
            for i in range(len(board)):
                x_cord = x_start + i
                y_cord = y_start + i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or x_cord == len(board) - 1:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []

    if direction == "up right to low left":
        if len(board) - y_start < x_start:
            for i in range(len(board) - x_start):
                x_cord = x_start + i
                y_cord = y_start - i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or x_cord == len(board) - 1:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []
        if len(board) - y_start > x_start:
            for i in range(y_start + 1):
                x_cord = x_start + i
                y_cord = y_start - i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or y_cord == 0:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []
        if len(board) - y_start == x_start:
            for i in range(len(board) - x_start):
                x_cord = x_start + i
                y_cord = y_start - i
                if board[x_cord][y_cord] == col:
                    res.append([x_cord, y_cord])
                if board[x_cord][y_cord] != col or y_cord == 0:
                    if len(res) == length:
                    # only want to look at sequences of length length
                        sequence_list.append(res)
                        res = []
                    if len(res) != length:
                        res = []


    # Checking the lists of sequences for open or semiopen
    open_seq_count = 0
    semi_open_seq_count = 0

    for i in range(len(sequence_list)):
        s_y_end = sequence_list[i][length - 1][1]
        s_x_end = sequence_list[i][length - 1][0]
        if is_bounded(board, s_y_end, s_x_end, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
        if is_bounded(board, s_y_end, s_x_end, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1

    return open_seq_count, semi_open_seq_count

# if __name__ == '__main__':
#     board = make_empty_board(8)
#     print_board(board)
#     board[1][5] = "w"
#     board[2][5] = "w"
#     board[3][5] = "w"
#     col = "w"
#     y_start = 7
#     x_start = 1
#     length = 2
#     d_y = 1
#     d_x = -1
#     print("(open, semi open)")
#     print(detect_row(board, col, y_start, x_start, length, d_y, d_x))

def detect_rows(board, col, length): # Done :D
    '''Return tuple whose first element is the number of open
    sequences of colour col of length length of the entire board,
    and whose second element is the number of semi-open sequences
    of colour col of length length on the entire board

    Only complete sequences count

    Assume length is an int >= 2
    '''
    open_seq_count, semi_open_seq_count = 0, 0

    # Empty list to store the results from each direction
        # detect_row() returns tuple containing (# of open, # of semiopen)
        # going to use list() function to convert tuple into a list so
        # it can be appended to the below list

    open_semiopen = []

    # Checking each direction:

    # Left to right
    d_y = 0
    d_x = 1
    y_start = 0
    for i in range(len(board)):
        x_start = i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))

    # Top to bottom
    d_y = 1
    d_x = 0
    x_start = 0
    for i in range(len(board)):
        y_start = i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))

    # Upper left to lower right
    d_y = 1
    d_x = 1
    # diagonal line splitting the board
    x_start = 0
    y_start = 0
    t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
    open_semiopen.append(list(t))
    # bottom of board (split diagonally from upper left to lower right)
    y_start = 0
    for i in range(1, len(board)):
        x_start = i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))
    # top of board (split diagonally from upper left to lower right)
    x_start = 0
    for i in range(1,len(board)):
        y_start = i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))

    # Upper right to lower left
    d_y = 1
    d_x = -1
    # diagonal line splitting the board
    x_start = 0
    y_start = len(board) - 1
    t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
    open_semiopen.append(list(t))
    # bottom of board (split diagonally from uppper right to lower left)
    y_start = len(board) - 1
    for i in range(1, len(board)):
        x_start = i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))
    # top of board (split diagonally from upper right to lower left)
    x_start = 0
    for i in range(1,len(board)):
        y_start = len(board) - 1 - i
        t = detect_row(board, col, y_start, x_start, length, d_y, d_x)
        open_semiopen.append(list(t))

    # Counting number of open sequences appended to list of list open_semiopen
    for i in range(len(open_semiopen)):
        open_seq_count += open_semiopen[i][0]
        semi_open_seq_count += open_semiopen[i][1]

    return open_seq_count, semi_open_seq_count

# if __name__ == '__main__':
#     board =  [[' ', 'b', 'b', 'b', 'b', 'b', 'b', ' '], [' ', ' ', ' ', 'w', 'b', 'b', 'w', ' '], ['w', 'w', 'w', 'w', 'b', 'w', 'b', ' '], ['w', 'w', 'w', 'b', 'b', 'w', 'w', 'b'], [' ', 'b', 'b', 'b', 'b', 'w', 'w', 'b'], ['w', ' ', ' ', 'b', ' ', ' ', ' ', 'w'], [' ', 'w', ' ', 'b', ' ', 'w', 'w', 'b'], [' ', 'b', 'b', 'b', 'b', 'b', 'b', 'b']]
#
#     print_board(board)
#     col = "w"
#     length = 2
#     print("(open, semi open)")
#     print(detect_rows(board, col, length))


def score(board): # Don't modify >:(
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def search_max(board): # Done :D
    '''Uses function score() to find optimal move for black. Finds
    location (y,x) s.t. (y,x) is empty and putting a balck stone on
    (y,x) maximizes the score of the board as calculated by score()

    Return tuple (y,x) s.t. score is maximized by putting a
    black stone there
        if there are multiple tuples then return any one of them

    After the function runs the contents of board must
    remain the same
    '''
    max_score = -100000
    move_y = 0
    move_x = 0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                board[i][j] = "b"
                if score(board) > max_score:
                    max_score = score(board)
                    move_y = i
                    move_x = j
                    board[i][j] = ' '
                else:
                    board[i][j] = ' '

    return move_y, move_x

# if __name__ == '__main__':
#     board = make_empty_board(8)
#     board[0][3] = "b"
#     board[1][3] = "b"
#     board[2][3] = "b"
#     board[4][3] = "b"
#     print_board(board)
#     print(search_max(board))

def is_win(board):
    '''Return one of the following: "White won", "Black won",
    "Draw", or "Continue playing"

    Return "Draw" iff the board is full and no winner
    '''
    # checking rows for white wins
    sequence_counter = 0
    for i in range(len(board)):
        sequence_counter = 0
        for j in range(len(board)):
            if board[i][j] == "w":
                sequence_counter += 1
            if board[i][j] != "w" or j == len(board) - 1:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking rows for black wins
    sequence_counter = 0
    for i in range(len(board)):
        sequence_counter = 0
        for j in range(len(board)):
            if board[i][j] == "b":
                sequence_counter += 1
            if board[i][j] != "b" or j == len(board) - 1:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0

    # checking columns for white wins
    sequence_counter = 0
    for i in range(len(board)):
        sequence_counter = 0
        for j in range(len(board)):
            if board[j][i] == "w":
                sequence_counter += 1
            if board[j][i] != "w" or j == len(board) - 1:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking columns for black wins
    sequence_counter = 0
    for i in range(len(board)):
        sequence_counter = 0
        for j in range(len(board)):
            if board[j][i] == "b":
                sequence_counter += 1
            if board[j][i] != "b" or j == len(board) - 1:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking up right to lower left diagonals for white wins
        # checking the center diagonal
    sequence_counter = 0
    for i in range(len(board)):
        x_cord = len(board) - 1 - i
        y_cord = i
        if board[x_cord][y_cord] == "w":
            sequence_counter += 1
        if board[x_cord][y_cord] != "w":
            if sequence_counter == 5:
                return "White won"
            if sequence_counter != 5:
                sequence_counter = 0
        if x_cord == 0:
            if sequence_counter == 5:
                return "White won"
            if sequence_counter != 5:
                sequence_counter = 0
        # checking top half of board split by diagonal
    sequence_counter = 0
    for i in range(4,6 + 1):
        if sequence_counter == 5:
            return "White won"
        sequence_counter = 0
        x_start = i
        for j in range(0, i + 1):
            if board[x_start - j][j] == "w":
                sequence_counter += 1
            if board[x_start - j][j] != "w" or x_start - j == 0:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
        # checking bottom half of board split by diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "White won"
        sequence_counter = 0
        y_start = i
        x_start = len(board) - 1
        for j in range(0, len(board) - i):
            if board[x_start - j][y_start + j] == "w":
                sequence_counter += 1
            if board[x_start - j][y_start + j] != "w" or y_start + j == len(board) - 1:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking upper right to lower left diagonals for black wins
        # checking the center diagonal
    sequence_counter = 0
    for i in range(len(board)):
        x_cord = len(board) - 1 - i
        y_cord = i
        if board[x_cord][y_cord] == "b":
            sequence_counter += 1
        if board[x_cord][y_cord] != "b":
            if sequence_counter == 5:
                return "Black won"
            if sequence_counter != 5:
                sequence_counter = 0
        if x_cord == 0:
            if sequence_counter == 5:
                return "Black won"
            if sequence_counter != 5:
                sequence_counter = 0
        # checking top half of board split by diagonal
    sequence_counter = 0
    for i in range(4,6 + 1):
        if sequence_counter == 5:
            return "Black won"
        sequence_counter = 0
        x_start = i
        for j in range(0, i + 1):
            if board[x_start - j][j] == "b":
                sequence_counter += 1
            if board[x_start - j][j] != "b" or x_start - j == 0:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0
        # checking bottom half of board split by diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "Black won"
        sequence_counter = 0
        y_start = i
        x_start = len(board) - 1
        for j in range(0, len(board) - i):
            if board[x_start - j][y_start + j] == "b":
                sequence_counter += 1
            if board[x_start - j][y_start + j] != "b" or y_start + j == len(board) - 1:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking up left to low right diagonals for white wins
        # checking the center diagonal
    sequence_counter = 0
    for i in range(len(board)):
        if board[i][i] == "w":
            sequence_counter += 1
        if board[i][i] != "w":
            if sequence_counter == 5:
                return "White won"
            if sequence_counter != 5:
                sequence_counter = 0
        if i == len(board) - 1:
            if sequence_counter == 5:
                return "White won"
            if sequence_counter != 5:
                sequence_counter = 0
        # checking bottom half below diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "White won"
        sequence_counter = 0
        x_start = i
        for j in range(len(board) - i):
            if board[i + j][j] == "w":
                sequence_counter += 1
            if board[i + j][j] != "w" or i + j == len(board) - 1:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
        # checking top half above diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "White won"
        sequence_counter = 0
        y_start = i
        for j in range(len(board) - i):
            if board[j][i + j] == "w":
                sequence_counter += 1
            if board[j][i + j] != "w" or i + j == len(board) - 1:
                if sequence_counter == 5:
                    return "White won"
                if sequence_counter != 5:
                    sequence_counter = 0
    # checking up left to low right diagonals for black wins
        # checking the center diagonal
    sequence_counter = 0
    for i in range(len(board)):
        if board[i][i] == "b":
            sequence_counter += 1
        if board[i][i] != "b":
            if sequence_counter == 5:
                return "Black won"
            if sequence_counter != 5:
                sequence_counter = 0
        if i == len(board) - 1:
            if sequence_counter == 5:
                return "Black won"
            if sequence_counter != 5:
                sequence_counter = 0
        # checking bottom half below diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "Black won"
        sequence_counter = 0
        x_start = i
        for j in range(len(board) - i):
            if board[i + j][j] == "b":
                sequence_counter += 1
            if board[i + j][j] != "b" or i + j == len(board) - 1:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0
        # checking top half above diagonal
    sequence_counter = 0
    for i in range(1,3 + 1):
        if sequence_counter == 5:
            return "Black won"
        sequence_counter = 0
        y_start = i
        for j in range(len(board) - i):
            if board[j][i + j] == "b":
                sequence_counter += 1
            if board[j][i + j] != "b" or i + j == len(board) - 1:
                if sequence_counter == 5:
                    return "Black won"
                if sequence_counter != 5:
                    sequence_counter = 0


    # checking for draw
    empty_space = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                empty_space += 1

    if empty_space == 0:
        return "Draw"

    # continue otherwise
    return "Continue playing"

#### DON'T EDIT BELOW

def print_board(board): # Don't modify >:(

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board): # Don't modify >:(
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size): # Don't modify >:(
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col): # Don't modify >:(
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", y, x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




# if __name__ == '__main__':
#     play_gomoku(8)
