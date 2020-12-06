ball_sz = [15, 15]
table_sz = [440, 280]
paddle_sz = [10, 70]
last_x = 0
last_y = 0

prev_x_position = 0.0
prev_y_position = 0.0



def paddle(x_position):
    return not (int(x_position) > 24 and int(x_position) < 400)

def frames(x_position, y_position, x_velocity, y_velocity, forward_movement):
    try:

        y_dis = 0
        longest_y = 0
        longest_x = 0

        if y_velocity < 0:
            y_dis = y_position + 1
            longest_y = int(y_dis / (-y_velocity * forward_movement) + 0.9999)

        else:
            y_dis = abs(266 - y_position)
            longest_y = int(y_dis / (y_velocity * forward_movement) + 0.9999)

        if x_velocity < 0:
            x_dis = abs(x_position - 25)
            longest_x = int(x_dis / (-x_velocity * forward_movement) + 0.9999)

        else:
            x_dis = abs(x_position - 400)
            longest_x = int(x_dis /  (x_velocity * forward_movement) + 0.9999)
        if longest_y < longest_x:
            return longest_y
        else:
            return longest_x
    except:
        return 11111111111

def collides(y_position):
    if int(y_position - 0.001) < 0 or int(y_position + 0.001) + 15 > 280:
        return True
    return False


def position_velocity(x_position, y_position, x_velocity, y_velocity):
    counter = 0
    max_counter = 10000
    backwards_movement = int(( x_velocity ** 2 + y_velocity ** 2) ** .5)
    forward_movement = 1


    if backwards_movement > 0:

        forward_movement = 1.0 / backwards_movement

    while not paddle(x_position):
        #print(x_position)
        counter += 1
        if counter > max_counter:
            break


        elif collides(y_position):
            counter2 = 0
            while collides(y_position):
                counter += 1
                x_position += -0.1 * x_velocity * forward_movement
                y_position += -0.1 * y_velocity * forward_movement
                counter2 += 1
                if counter > max_counter:
                    break

            y_velocity = -y_velocity
            while counter2 > 0 or collides(y_position):
                counter += 1
                x_position += 0.1 * x_velocity * forward_movement
                y_position += 0.1 * y_velocity * forward_movement
                counter2 -= 1
                if counter > max_counter:
                    break
        else:
            skipper = frames(x_position, y_position, x_velocity, y_velocity, forward_movement)
            x_position += x_velocity * forward_movement * skipper
            y_position += y_velocity * forward_movement * skipper

    return y_position


def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global prev_x_position, prev_y_position

    position_ball, paddle_pos = ball_frect.pos, paddle_frect.pos
    ball_x_velocity = position_ball[0] - prev_x_position
    ball_y_velocity = position_ball[1] - prev_y_position
    prev_x_position, prev_y_position = position_ball[0], position_ball[1]
    direction = 1

    if paddle_pos[0] < other_paddle_frect.pos[0]:
        direction = -1

    if ball_x_velocity == 0:
        ball_x_velocity = 1
    ball_dir = ball_x_velocity / abs(ball_x_velocity)

    if direction == ball_dir:
        position = position_velocity(position_ball[0], position_ball[1], ball_x_velocity, ball_y_velocity)
        paddle_placement = position - paddle_sz[1] / 2
        #print(position)
    else:
        paddle_placement = 210 / 2

    if paddle_placement > paddle_pos[1]:
        return "down"

    else:
        return "up"