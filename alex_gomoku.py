


def is_empty(board):
    check = True
    for r in board:
        for b in r:
            if(b != ' '):
                check = False
                break
    return check

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    rh_occupied = False
    lh_occupied = False

    lh_y = y_end - d_y * length
    lh_x = x_end - d_x * length

    if not is_on_board(y_end + d_y, x_end + d_x) or board[y_end + d_y][x_end + d_x] != ' ':
        rh_occupied = True

    if not is_on_board(lh_y, lh_x) or board[lh_y][lh_x] != ' ':
        lh_occupied = True

    if not lh_occupied and not rh_occupied:
        return "OPEN"
        
    elif (lh_occupied and not rh_occupied) or (not lh_occupied and rh_occupied):
        return "SEMIOPEN"
    elif lh_occupied and rh_occupied:
        return "CLOSED"


def is_on_board(y_cor, x_cor):
    if y_cor >= 0 and y_cor < 8 and x_cor >= 0 and x_cor < 8:
        return True
    else:
        return False


def detect_row(board, color, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    num_col_pieces = 0
    counter = 0

    right_coor_y = y_start + d_y * counter  ###COME BACK TO HERE DOES COUNTER ALWAYS EQUAL ZERO??
    right_coor_x = x_start + d_x * counter
    while 8 > right_coor_y > -1 and 8 > right_coor_x > -1:
        TorF = True
        if board[right_coor_y][right_coor_x] == color:
            num_col_pieces += 1
        if counter >= length - 1:
            left_coor_y = right_coor_y - (d_y * (length - 1))
            left_coor_x = right_coor_x - (d_x * (length - 1))

            y_check1 = right_coor_y + d_y
            x_check1 = right_coor_x + d_x
            y_check2 = left_coor_y - d_y
            x_check2 = left_coor_x - d_x

            if 8 > y_check2 >= 0 and 8 > x_check2 >= 0 and board[y_check2][x_check2] == color:
                TorF = False
            if 8 > y_check1 >= 0 and 8 > x_check1 >= 0 and board[y_check1][x_check1] == color:
                TorF = False

            if num_col_pieces == length:
                if TorF:
                    if is_bounded(board, right_coor_y, right_coor_x, length, d_y, d_x) == "OPEN":
                        # print(y_start,x_start)
                        open_seq_count += 1
                    elif is_bounded(board, right_coor_y, right_coor_x, length, d_y, d_x) == "SEMIOPEN":
                        # print(y_start, x_start)
                        semi_open_seq_count += 1

            if board[left_coor_y][left_coor_x] == color:
                num_col_pieces = num_col_pieces - 1

        counter += 1
        right_coor_y = y_start + d_y * counter
        right_coor_x = x_start + d_x * counter

    return open_seq_count, semi_open_seq_count

def detect_row_for_win(board, color, y_start, x_start, length, d_y, d_x):
    count = 0

    num_col_pieces = 0
    counter = 0

    right_coor_y = y_start + d_y * counter  ###COME BACK TO HERE DOES COUNTER ALWAYS EQUAL ZERO??
    right_coor_x = x_start + d_x * counter
    while 8 > right_coor_y > -1 and 8 > right_coor_x > -1:
        TorF = True
        if board[right_coor_y][right_coor_x] == color:
            num_col_pieces += 1
        if counter >= length - 1:
            left_coor_y = right_coor_y - (d_y * (length - 1))
            left_coor_x = right_coor_x - (d_x * (length - 1))

            y_check1 = right_coor_y + d_y
            x_check1 = right_coor_x + d_x
            y_check2 = left_coor_y - d_y
            x_check2 = left_coor_x - d_x

            if 8 > y_check2 >= 0 and 8 > x_check2 >= 0 and board[y_check2][x_check2] == color:
                TorF = False
            if 8 > y_check1 >= 0 and 8 > x_check1 >= 0 and board[y_check1][x_check1] == color:
                TorF = False

            if num_col_pieces == length:
                if TorF:
                    return 1

            if board[left_coor_y][left_coor_x] == color:
                num_col_pieces = num_col_pieces - 1

        counter += 1
        right_coor_y = y_start + d_y * counter
        right_coor_x = x_start + d_x * counter

    return 0

def detect_rows(board, color, length):
    open_seq = 0
    semi_seq = 0
    for i in range(len(board)):

        temp_list = detect_row(board, color, i, 0, length, 0, 1)

        open_seq += temp_list[0]
        semi_seq += temp_list[1]


        temp_list = detect_row(board, color, 0, i, length, 1, 0)

        open_seq += temp_list[0]
        semi_seq += temp_list[1]

        temp_list = detect_row(board, color, 0, i, length, 1, 1)
        open_seq += temp_list[0]
        semi_seq += temp_list[1]

        temp_list = detect_row(board, color, len(board) - 1, i, length, -1, 1)
        open_seq += temp_list[0]
        semi_seq += temp_list[1]

        if i != 0:
            temp_list = detect_row(board, color, i, 0, length, 1, 1)
            open_seq += temp_list[0]
            semi_seq += temp_list[1]
            temp_list = detect_row(board, color, len(board) - i - 1, 0, length, -1, 1)
            open_seq += temp_list[0]
            semi_seq += temp_list[1]
    return open_seq, semi_seq

def detect_rows_for_win(board, color, length):
    seq = 0
    for i in range(len(board)):

        seq += detect_row_for_win(board, color, i, 0, length, 0, 1)
        seq += detect_row_for_win(board, color, 0, i, length, 1, 0)
        seq += detect_row_for_win(board, color, 0, i, length, 1, 1)
        seq += detect_row_for_win(board, color, len(board) - 1, i, length, -1, 1)
        if i != 0:
            seq += detect_row_for_win(board, color, i, 0, length, 1, 1)
            seq += detect_row_for_win(board, color, len(board) - i - 1, 0, length, -1, 1)
    return seq


def search_max(board):
    best_move_y = -999999
    best_move_x = -999999
    best_score = 0

    for x_move in range(len(board)):
        for y_move in range(len(board)):
            if board[y_move][x_move] == " ":
                board[y_move][x_move] = 'b'
                temp = score(board)
                board[y_move][x_move] = ' '
                if temp >= best_score:  #maybe should be just greater than ?????
                    best_score = temp
                    best_move_y = y_move
                    best_move_x = x_move

    return best_move_y, best_move_x

def is_win(board):
    # come back to this part for full condition maybe
    full = True
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == ' ':
                full = False

    if full:
        return "Draw"
    if detect_rows_for_win(board, 'w', 5):
        return "White won"
    elif detect_rows_for_win(board, 'b', 5):
        return "Black won"
    else:
        return "Continue playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def score(board):
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

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def play_gomoku(board_size):
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

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
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
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def test_search_max():
    board = make_empty_board(8)
    x = 5;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
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
    y = 5;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 3
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

    y = 3;
    x = 5;
    d_x = -1;
    d_y = 1;
    length = 2

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

    y = 5;
    x = 3;
    d_x = -1;
    d_y = 1;
    length = 1
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


if __name__ == '__main__':
    easy_testset_for_main_functions()
