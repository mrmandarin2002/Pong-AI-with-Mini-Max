
table_size = [440, 280]
paddle_size = [10, 70]
ball_size = [15, 15]

prev_pos_x = 0
prev_pos_y = 0

def paddle_collision(pos_x):

    if pos_x < -10 or pos_x > 450:
        return False

    return not int(pos_x + 0.01) > 24 and int(pos_x - 0.01) < 400

def skip(pos_x, pos_y, vel_x, vel_y, move_factor):
    try:
        #walls
        dis_to_wall = 0
        y_max = 0
        x_max = 0
        if(vel_y < 0):
            dis_to_wall = pos_y + 1
            y_max = int((dis_to_wall / (-vel_y * move_factor)) + 0.999999)
        else:
            dis_to_wall = abs(266 - pos_y)
            y_max = int((dis_to_wall / (vel_y * move_factor)) + 0.999999)
        if(vel_x < 0):
            dis_to_paddle = abs(pos_x - 25) 
            x_max = int((dis_to_paddle) / (-vel_x * move_factor) + 0.999999)
        else:
            dis_to_paddle = abs(pos_x - 400)
            x_max = int((dis_to_paddle) / (vel_x * move_factor) + 0.999999)
        return min(y_max, x_max)
    except:
        return 1e9

def wall_collision(self, pos_y):
    return (int(pos_y - 0.001) < 0 or (int(pos_y + 0.001) + 15 > 280))


def ball_final(pos_x, pos_y, vel_x, vel_y):

    inv_move_factor = int((vel_x**2+vel_y**2)**.5)
    move_factor = 1

    if inv_move_factor > 0:
        move_factor = 1.0 / inv_move_factor

    looped = 0

    while not paddle_collision(pos_x):
        looped += 1
        if int(pos_y - 0.01) < 0 or int(pos_y + 0.01) + ball_size[1] > table_size[1]:
            c = 0 
            while int(pos_y - 0.01) < 0 or int(pos_y + 0.01) + ball_size[1] > table_size[1]:  
                looped += 1
                pos_x += -0.1 * vel_x * move_factor
                pos_y += -0.1 * vel_y * move_factor
                c = c + 1
                if looped > 1000:
                    break

            vel_y = -vel_y
            while c > 0 or int(pos_y - 0.01) < 0 or int(pos_y + 0.01) + ball_size[1] > table_size[1]:
                looped += 1
                pos_x += 0.1 * vel_x * move_factor
                pos_y += 0.1 * vel_y * move_factor
                c = c - 1
                if looped > 1000:
                    break
            if looped > 1000:
                break
        else:
            #print("ARRIVED")
            skip_num = skip(pos_x, pos_y, vel_x, vel_y, move_factor)
            pos_x += vel_x * move_factor * skip_num
            pos_y += vel_y * move_factor * skip_num
            if looped > 1000:
                break

    print("ARRIVE")

    return pos_y

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global prev_pos_x, prev_pos_y


    ball_pos = ball_frect.pos
    paddle_pos = paddle_frect.pos
    ball_vel_x = ball_pos[0] - prev_pos_x
    ball_vel_y = ball_pos[1] - prev_pos_y
    prev_pos_x = ball_pos[0]
    prev_pos_y = ball_pos[1]
    paddle_dir = 1

    if paddle_pos[0] < other_paddle_frect.pos[0]:
        paddle_dir = -1

    ball_dir = ball_vel_x / abs(ball_vel_x) 
    paddle_placement = 105 #where the paddle goes

    #print(paddle_dir, int(ball_dir))

    if paddle_dir == ball_dir:
        ball_final_pos = ball_final(ball_pos[0], ball_pos[1], ball_vel_x, ball_vel_y)
        paddle_placement = ball_final_pos - paddle_size[1] / 2
    else:
        paddle_placement = 105

    if paddle_placement > paddle_pos[1]:
        return "down"
    else:
        return "up"
        
