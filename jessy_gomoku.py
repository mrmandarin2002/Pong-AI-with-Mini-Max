#Project 2 - ESC180

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

board = make_empty_board(8)

#PRINT BOARD FUNCTION:
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

#SCORE BOARD FUNCTION:
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

#PLAY GOMOKU(BOARD_SIZE) FUNCTION:
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

#PUT SEQUENCE ON BOARD FUNCTION:
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

#ANALYSIS BOARD FUNCTION:
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                pass
            if board[i][j] != " ":
                return False
    return True


#Going forwards:
# 0, 1 (right, left)
# 1, 0 (downwards)
# 1, 1 (diagonally down right)
# 1, -1 (diagonally down left)


#checks if coordinates are inside the board
def reading_of_boundaries(y, x):
    if y >= 0 and y <= 7 and x >= 0 and x <= 7:
        return True
    else:
        return False


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    left_corner_x = x_end - d_x*length
    left_corner_y = y_end - d_y*length
    open_on_right, open_on_left = True, True
    #same idea as left_corners
    right_corner_y = y_end + d_y
    right_corner_x = x_end + d_x
    if reading_of_boundaries(right_corner_y, right_corner_x) == False or board[right_corner_y][right_corner_x] != ' ':
        #meaning that the rightmost point in the sequence is not within the length of the board,
        #then the sequence is closed on the right side
        #or if the right square is empty
        open_on_right = False
    if reading_of_boundaries(left_corner_y, left_corner_x) == False or board[left_corner_y][left_corner_x] != ' ':
        # meaning that the leftmost point in the sequence is not within the length of the board,
        # then the sequence is closed on the left side
        #or if the right square is empty
       open_on_left = False

    if open_on_left and open_on_right:
        return "OPEN"

    if open_on_left != open_on_right:
        return "SEMIOPEN"

    else:
        return "CLOSED"


#The function returns a tuple
# whose first element is the number of open sequences of colour col of length length in the row R,
# and whose second element is the number of semi-open sequences of colour col of length "length" in the row R
    #for loop that applies the

#Going forwards:
# 0, 1 (right, left)
# 1, 0 (downwards)
# 1, 1 (diagonally down right)
# 1, -1 (diagonally down left)

'''
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    counting_open_sequences = 0
    semi_open_sequences_counter = 0
    counter = 0
    for row in range(len(board)):

        if board[y_start][x_start] == col:
            counter += 1
        elif board[y_start][x_start] != col:
            counter = 0

        if counter == length:
            if (d_y == 1 and d_x == 1) or (d_y == 1 and d_x == -1): #FOR DIAGONALS
                if is_bounded(board, y_start, x_start, length, d_y, d_x) == "OPEN":
                    counting_open_sequences += 1
                elif is_bounded(board, y_start, x_start, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_sequences_counter += 1
            if d_y == 0 and d_x == 1: #FOR HORIZONTALS
                if is_bounded(board, y_start, x_start, length, d_y, d_x) == "OPEN":
                    counting_open_sequences += 1
                elif is_bounded(board, y_start, x_start, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_sequences_counter += 1
            if d_y == 1 and d_x == 0: #FOR VERTICALS
                if is_bounded(board, y_start, x_start, length, d_y, d_x) == "OPEN":
                    counting_open_sequences += 1
                elif is_bounded(board, y_start, x_start, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_sequences_counter += 1
        
        if y_start < len(board)-1:
            y_start += d_y
            if x_start < len(board)-1:
                if d_x == -1 and x_start == 0:
                    continue
                x_start += d_x

    
    return counting_open_sequences, semi_open_sequences_counter
'''

def detect_row(board, color, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    if(color == 'b'):
        pass
        #print(y_start, x_start, d_y, d_x, "LENGTH:", length)
    r_idx = 0
    piece_cnt = 0
    right_cor =  (y_start + d_y * r_idx, x_start + d_x * r_idx)
    while(7 >= right_cor[0] >= 0 and 7 >= right_cor[1] >= 0):
        if(board[right_cor[0]][right_cor[1]] == color):
            piece_cnt += 1
        if(r_idx >= length - 1):
            check = True
            left_cor = (right_cor[0] - d_y * (length - 1), right_cor[1] - d_x * (length - 1))
            if(reading_of_boundaries(right_cor[0] + d_y, right_cor[1] + d_x) and board[right_cor[0] + d_y][right_cor[1] + d_x] == color):
                check = False
            elif(reading_of_boundaries(left_cor[0] - d_y, left_cor[1] - d_x) and board[left_cor[0] - d_y][left_cor[1] - d_x] == color):
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


#This function analyses the board board. The function returns a tuple with:
# Element 1: number of open sequences of colour col of length length on the entire board,
# Element 2: number of semi-open sequences of colour col of length length on the entire board.
# Only complete sequences count.
# Assume length is an integer greater or equal to 2
# detect_row(board, col, y_start, x_start, length, d_y, d_x)
#def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    # for i in range(length):
    #     board[y][x] = col
    #     y += d_y
    #     x += d_x

def detect_rows(board, col, length):
    counting_open_sequences, semi_open_sequences_counter = (0, 0)

    for i in range(len(board) - 1): #check diagonals moving across the columns. right to left (1,1)
        counting_open_sequences += detect_row(board, col, 0, i, length, 1, 1)[0]
        semi_open_sequences_counter += detect_row(board, col, 0, i, length, 1, 1)[1]

    for i in range(len(board) - 1): #check diagonals moving down the rows. up to down  (1,1)
        if(i != 0):
            counting_open_sequences += detect_row(board, col, i, 0, length, 1, 1)[0]
            semi_open_sequences_counter += detect_row(board, col, i, 0, length, 1, 1)[1]

    for i in range(len(board) - 1): #check diagonals moving from right to left across columns. (1,-1)
        counting_open_sequences += detect_row(board, col, 0, i, length, 1, -1)[0]
        semi_open_sequences_counter += detect_row(board,col,  0, i, length, 1, -1)[1]

    for i in range(len(board) - 1): #check all the diagonal moving from right to left. up to down. (1, -1)
        if(i != 7):
            counting_open_sequences += detect_row(board, col, i, 7, length, 1, -1)[0]
            semi_open_sequences_counter += detect_row(board, col, i, 7, length, 1, -1)[1]

    #THIS WORKS GREAT
    for i in range(len(board)): #check all the horizontal
        counting_open_sequences += detect_row(board, col, i, 0, length, 0, 1)[0]
        semi_open_sequences_counter += detect_row(board, col, i, 0, length, 0, 1)[1]

    for i in range(len(board)): #check all the vertical
        counting_open_sequences += detect_row(board, col, 0, i, length, 1, 0)[0]
        semi_open_sequences_counter += detect_row(board, col, 0, i, length, 1, 0)[1]

    return counting_open_sequences, semi_open_sequences_counter



def search_max(board):
    # A function which places a "b" marker down on every square, uses the score function to return a score internally
    # Appending the marker position to a list
    # Appending the score with respect to that marker to the list.
    # Then finding the max value of the list for scores achieved; and the index attributed to the score via the list black_positions
    black_positions = []
    score_of_black = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                put_seq_on_board(board, i, j, 0, 0, 1, "b")
                score_of_black.append(score(board))
                black_positions.append((i, j))
                put_seq_on_board(board, i, j, 0, 0, 1, " ")

            if board[i][j] != " ":
                pass

    max_score = max(score_of_black)
    for i in range(len(score_of_black)):
        if max_score == score_of_black[i]:
            ind_value = i
            break
    return black_positions[i][0],  black_positions[i][1]


###################################################IS WIN FUNCTION######################################################################

# HORIZONTAL CHECK
def is_horizontal_win(board):
    for i in range(len(board)):
        w_count = 0
        b_count = 0
        for j in range(len(board[i])):
            if board[i][j] == "w":
                w_count += 1
                b_count = 0

            if board[i][j] == "b":
                b_count += 1
                w_count = 0

            if board[i][j] == " ":
                b_count = 0
                w_count = 0

            if b_count == 5:
                return "Black won"

            if w_count == 5:
                return "White won"

#VERTICAL CHECK
def is_vertical_win(board):
    for j in range(len(board[1])):
        w_count = 0
        b_count = 0
        for i in range(len(board)):
            if board[i][j] == "w":
                w_count += 1
                b_count = 0

            if board[i][j] == "b":
                b_count += 1
                w_count = 0

            if board[i][j] == " ":
                b_count = 0
                w_count = 0

            if b_count == 5:
                return "Black won"

            if w_count == 5:
                return "White won"



#DIAGONAL CHECK
def is_diag_l_win(board):
    for i in range(8):
        w_count = 0
        b_count = 0
        temp = 0
        for j in range(len(board)):
            if board[i][j] == "w":
                w_count += 1
                b_count = 0
                i += 1
                temp += 1

            elif board[i][j] == "b":
                b_count += 1
                w_count = 0
                i += 1
                temp += 1

            elif board[i][j] == " ":
                b_count = 0
                w_count = 0
                i -= temp

            if b_count == 5:
                return "Black won"

            if w_count == 5:
                return "White won"

def is_diag_r_win(board):
    for i in range(8):
        w_count = 0
        b_count = 0
        temp = 0
        for j in range(len(board)-1,-1,-1):
            if board[i][j] == "w":
                w_count += 1
                b_count = 0
                i += 1
                temp += 1

            elif board[i][j] == "b":
                b_count += 1
                w_count = 0
                i += 1
                temp += 1

            elif board[i][j] == " ":
                b_count = 0
                w_count = 0
                i -= temp

            if b_count == 5:
                return "Black won"

            if w_count == 5:
                return "White won"


#Final Check for Draw
def is_draw(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                break
            if board[7][7] != " ":
                return "Draw"



def is_win(board):
    if is_horizontal_win(board) != None:
        return is_horizontal_win(board)

    if is_vertical_win(board) != None:
        return is_vertical_win(board)

    if is_diag_l_win(board) != None:
        return is_diag_l_win(board)

    if is_diag_r_win(board) != None:
        return is_diag_r_win(board)

    if is_draw(board) != None:
        return is_draw(board)

    else:
        return "Continue playing"



if __name__== "__main__":
    put_seq_on_board(board, 1, 1, 0, 1, 2, "w")
    put_seq_on_board(board, 3, 6, 0, 1, 1, "w")
    put_seq_on_board(board, 0, 3, 0, 1, 3, "w")
    put_seq_on_board(board, 6, 6, 0, 1, 1, "w")
    put_seq_on_board(board, 2, 3, 1, 1, 3, "w")
    put_seq_on_board(board, 7, 4, 0, 1, 4, "w")
    put_seq_on_board(board, 2, 5, 0, 1, 2, "w")
    put_seq_on_board(board, 0, 6, 0, 1, 1, "b")
    put_seq_on_board(board, 7, 2, 0, 1, 2, "b")
    put_seq_on_board(board, 2, 2, 1, 1, 4, "b")
    put_seq_on_board(board, 3, 2, 1, 1, 3, "b")
    put_seq_on_board(board, 3, 1, 1, 1, 3, "b")
    put_seq_on_board(board, 0, 7, 1, 0, 3, "b")
    put_seq_on_board(board, 6, 0, 0, 1, 2, "b")
    put_seq_on_board(board, 2, 0, 1, 0, 3, "b")
    print_board(board)
    analysis(board)
    ###Function Arbitrary Testings
    print(is_empty(board))
    print(is_bounded(board, 5, 5, 4, 1, 1))
    print(detect_row(board, "b", 2, 2, 3, 1, 0))
    print(detect_rows(board, "w", 3))
    print(search_max(board))
    # print(is_win(board))
















