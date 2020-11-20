"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for row in board:
        for box in row:
            if(box != ' '):
                return False
    return True

def check_within_bounds(y, x):
    if(y >= 0 and y <= 7 and x >= 0 and x <= 7):
        return True
    else:
        return False
        
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    right_closed, left_closed = False, False
    left_cor_x = x_end - d_x * length
    left_cor_y = y_end - d_y * length
    if(not check_within_bounds(y_end + d_y, x_end + d_x) or board[y_end + d_y][x_end + d_x] != ' '):
        right_closed = True
    if(not check_within_bounds(left_cor_y, left_cor_x) or board[left_cor_y][left_cor_x] != ' '):
        left_closed = True
    if(not left_closed and not right_closed):
        return "OPEN"
    elif(left_closed != right_closed):
        return "SEMIOPEN"
    else:
        return "CLOSED"
        
#test_boards
test_board1 = [[' ', ' ', ' ', ' ', ' ', ' ', 'b', ' '], 
                [' ', ' ', ' ', ' ', ' ', 'b', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                ['b', 'b', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            ]

#print("TEST: ", is_bounded(test_board1, 7, 1, 8, 1, 0))

white_closed = 0
black_closed = 0

#aLWaYs TeSt CoDE YEEEEEEEEEEEEEEEEEEEE
def detect_row(board, color, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    r_idx = 0
    piece_cnt = 0
    right_cor = (y_start, x_start)
    while(7 >= right_cor[0] >= 0 and 7 >= right_cor[1] >= 0):
        #print(right_cor)
        if(board[right_cor[0]][right_cor[1]] == color):
            piece_cnt += 1
        if(r_idx >= length - 1):
            #makes sure that the sequence is not actually larger
            check = True
            left_cor = (right_cor[0] - d_y * (length - 1), right_cor[1] - d_x * (length - 1))
            #print("RIGHT COR:", right_cor)
            #print("LEFT_COR:", left_cor)
            if(check_within_bounds(right_cor[0] + d_y, right_cor[1] + d_x) and board[right_cor[0] + d_y][right_cor[1] + d_x] == color):
                check = False
            elif(check_within_bounds(left_cor[0] - d_y, left_cor[1] - d_x) and board[left_cor[0] - d_y][left_cor[1] - d_x] == color):
                check = False

            if(piece_cnt == length and check):
                seq_status = is_bounded(board, right_cor[0], right_cor[1], length, d_y, d_x)
                if(seq_status == "OPEN"):
                    open_seq_count += 1
                elif(seq_status == "SEMIOPEN"):
                    semi_open_seq_count += 1

            if(board[left_cor[0]][left_cor[1]] == color):
                piece_cnt -= 1

        r_idx += 1
        right_cor = (y_start + d_y * r_idx, x_start + d_x * r_idx)
        
    return open_seq_count, semi_open_seq_count

def detect_row_returns_closed(board, color, y_start, x_start, length, d_y, d_x):
    seq_count = 0
    r_idx = 0
    piece_cnt = 0
    right_cor =  (y_start + d_y * r_idx, x_start + d_x * r_idx)

    while(7 >= right_cor[0] >= 0 and 7 >= right_cor[1] >= 0):
        #print(right_cor)
        if(board[right_cor[0]][right_cor[1]] == color):
            piece_cnt += 1
        if(r_idx >= length - 1):
            check = True
            left_cor = (right_cor[0] - d_y * (length - 1), right_cor[1] - d_x * (length - 1))
            #print("RIGHT COR:", right_cor)
            #print("LEFT_COR:", left_cor)
            if(check_within_bounds(right_cor[0] + d_y, right_cor[1] + d_x) and board[right_cor[0] + d_y][right_cor[1] + d_x] == color):
                check = False
            elif(check_within_bounds(left_cor[0] - d_y, left_cor[1] - d_x) and board[left_cor[0] - d_y][left_cor[1] - d_x] == color):
                check = False
            if(piece_cnt == length and check):
                seq_count += 1
            if(board[left_cor[0]][left_cor[1]] == color):
                piece_cnt -= 1
        r_idx += 1
        right_cor = (y_start + d_y * r_idx, x_start + d_x * r_idx)
    return seq_count
    
def sum_lists(list1, list2):
    return [x + y for x, y in zip(list1, list2)]

def detect_rows_win(board, color, length):
    #index 0 - open_seq_count
    #index 1 - semi_open_seq_count
    seq_cnt = 0
    for i in range(len(board)):

        seq_cnt += detect_row_returns_closed(board, color, i, 0, length, 0, 1) #left to right
        seq_cnt += detect_row_returns_closed(board, color, 0, i, length, 1, 0) #up to down

        # --- diagonals ---
        seq_cnt += detect_row_returns_closed(board, color, 0, i, length, 1, 1) #upper-left to lower right
        seq_cnt += detect_row_returns_closed(board, color, len(board) - 1, i, length, -1, 1) #lower-left to upper right
        ### why the actual fuck is x referring to cols and y referring to rows ?????????
        if(i != 0): #so we don't count the same diagonals twice
            seq_cnt += detect_row_returns_closed(board, color, i, 0, length, 1, 1)

            seq_cnt += detect_row_returns_closed(board, color, len(board) - 1 - i, 0, length, -1, 1)

    return seq_cnt

def detect_rows(board, color, length):
    #index 0 - open_seq_count
    #index 1 - semi_open_seq_count
    seq_cnt = [0,0] 
    for i in range(len(board)):
        seq_cnt = sum_lists(seq_cnt, detect_row(board, color, i, 0, length, 0, 1)) #left to right
        seq_cnt = sum_lists(seq_cnt, detect_row(board, color, 0, i, length, 1, 0)) #up to down

        # --- diagonals ---
        seq_cnt = sum_lists(seq_cnt, detect_row(board, color, 0, i, length, 1, 1)) #upper-left to lower right
        seq_cnt = sum_lists(seq_cnt, detect_row(board, color, len(board) - 1, i, length, -1, 1)) #lower-left to upper right
        ### why the actual fuck is x referring to cols and y referring to rows ?????????
        if(i != 0): #so we don't count the same diagonals twice
            seq_cnt = sum_lists(seq_cnt, detect_row(board, color, i, 0, length, 1, 1))
            seq_cnt = sum_lists(seq_cnt, detect_row(board, color, len(board) - 1 - i, 0, length, -1, 1))

    return seq_cnt[0], seq_cnt[1]
    
def search_max(board):
    cor = [-1, -1]
    max_score = -1e9
    for y in range(len(board)):
        for x in range(len(board)):
            if(board[y][x] == ' '):
                board[y][x] = 'b'
                cur_score = score(board)
                if(max_score < cur_score):
                    max_score = cur_score
                    cor[0], cor[1] = y, x
                board[y][x] = ' '
    return cor[0], cor[1]

def is_full(board):
    cnt = 0
    for y in range(len(board)):
        for x in range(len(board)):
            if(board[y][x] == ' '):
                cnt += 1
    return cnt == len(board) ** 2

def is_win(board):
    if(is_full(board)):
        return "Draw"
    white_cnt = detect_rows_win(board, 'w', 5)
    black_cnt = detect_rows_win(board, 'b', 5)
    if(black_cnt != 0 and white_cnt != 0): #remove this line for gradescope submission
        return "Impossible"
    if(white_cnt != 0):
        return "White won"
    elif(black_cnt != 0):
        return "Black won"
    else:
        return "Continue playing"
    
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
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def print_board(board):
    
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

def analysis(board):
    return_value = []
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        #print("%s stones" % (full_name))
        return_value.append(str("%s stones" % (full_name)))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            #print("Open rows of length %d: %d" % (i, open))
            #print("Semi-open rows of length %d: %d" % (i, semi_open))
            return_value.append(str("Open rows of length %d: %d" % (i, open)))
            return_value.append(str("Semi-open rows of length %d: %d" % (i, semi_open)))
    return return_value
    
        
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
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
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


def testing_win_5_closed():
    board = make_empty_board(8)
    board[2][2] = "w"
    y = 3;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    if is_win(board)=="Black won":
        print("PASSSSSSSSS")
    else:
        print("EPIC FAIL :(")
        # Expected output:
        # *0|1|2|3|4|5|6|7*
        # 0 | | | | | | | *
        # 1 | | | | | | | *
        # 2 | |w| | | | | *
        # 3 | |b| | | | | *
        # 4 | |b| | | | | *
        # 5 | |b| | | | | *
        # 6 | |b| | | | | *
        # 7 | |b| | | | | *
        # *****************
        # PASSSSSSSSS


if __name__ == '__main__':
    #testing_win_5_closed()
    case_1 = [
        [' ', ' ', 'w', 'w', 'w', ' ', 'b', 'b'],
        ['w', 'w', 'w', 'w', 'w', 'b', 'b', ' '],
        ['w', 'w', ' ', ' ', 'b', ' ', 'b', 'b'],
        ['w', ' ', ' ', 'b', ' ', 'w', 'b', ' '],
        [' ', 'b', 'w', ' ', 'w', 'w', 'w', 'b'],
        ['b', ' ', 'w', 'w', ' ', 'w', 'b', ' '],
        ['b', ' ', 'w', 'w', ' ', 'b', 'w', ' '],
        [' ', ' ', 'w', ' ', 'b', 'w', 'w', 'w']
    ]
    print(test_search_max())
    pass
    #easy_testset_for_main_functions()
    #some_tests()
    #play_gomoku(8)
    '''
    board = []
    for i in range(8):
        board.append([" "]*8)
    put_seq_on_board(board, 0, 0, 0, 1, 1, "w")
    put_seq_on_board(board, 1, 1, 0, 1, 2, "w")
    put_seq_on_board(board, 3, 6, 0, 1, 1, "w")
    put_seq_on_board(board, 0, 3, 0, 1, 3, "w")
    put_seq_on_board(board, 6, 6, 0, 1, 1, "w")
    put_seq_on_board(board, 2, 3, 1, 1, 3, "w")
    put_seq_on_board(board, 7, 4, 0, 1, 4, "w")
    put_seq_on_board(board, 2, 5, 0, 1, 2, "w")
    put_seq_on_board(board, 5, 2, 1, 1, 2, "w")
    put_seq_on_board(board, 7, 0, 0, 1, 1, "b")
    put_seq_on_board(board, 0, 6, 0, 1, 1, "b")
    put_seq_on_board(board, 7, 2, 0, 1, 2, "b")
    put_seq_on_board(board, 2, 2, 1, 1, 4, "b")
    put_seq_on_board(board, 3, 2, 1, 1, 3, "b")
    put_seq_on_board(board, 3, 1, 1, 1, 3, "b")
    put_seq_on_board(board, 0, 7, 1, 0, 3, "b")
    put_seq_on_board(board, 6, 0, 0, 1, 2, "b")
    put_seq_on_board(board, 2, 0, 1, 0, 3, "b")
    put_seq_on_board(board, 3, 5, 1, 1, 3, "b")
    put_seq_on_board(board, 1, 4, 0, 1, 2, "b")
    print_board(board)
    analysis(board)
    '''