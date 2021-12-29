thread_running = False
client_thread = None
scratch_img = None
my_index = None

import socket, threading
from urllib import request
import pygame, inspect, math, json


def replacement_render(screen, paddles, ball, score, table_size):
    global scratch_img
    screen.fill(black)
    pygame.draw.rect(screen, white, paddles[0].frect.get_rect())
    pygame.draw.rect(screen, white, paddles[1].frect.get_rect())
    pygame.draw.circle(screen, white, (int(ball.get_center()[0]), int(ball.get_center()[1])),  int(ball.frect.size[0]/2), 0)
    pygame.draw.line(screen, white, [screen.get_width()/2, 0], [screen.get_width()/2, screen.get_height()])
    score_font = pygame.font.Font(None, 32)
    screen.blit(score_font.render(str(score[0]), True, white), [int(0.4*table_size[0])-8, 0])
    screen.blit(score_font.render(str(score[1]), True, white), [int(0.6*table_size[0])-8, 0])
    width = ball.frect.size[0]*2
    height = int(ball.frect.size[0]*1.503472222)
    try:
        screen.blit(pygame.transform.scale(scratch_img, (width, height)), (int(ball.get_center()[0]-width/2), int(ball.get_center()[1]-height/2)))
    except:
        try:
            scratch_img = pygame.image.load("scratch.png")
        except:
            pass
    pygame.display.flip()

class Network:

    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST_IP 
        self.addr = (self.host, PORT)
        self.id = self.connect()

    def connect(self):
        self.conn.connect(self.addr)
        self.conn.send(str.encode('game'))
        received_message = self.conn.recv(2048).decode()
        return received_message

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.conn.send(str.encode(data))
        except socket.error as e:
            return str(e)

kill = False
scratch = False
scratch_executed = True
opponent_function = None
old_opponent_code = None
old_render_code = None
has_downloaded = False
god_mode = False
opponent_hit_tracker = []

hax_thread = None
first_run = True

# get render function object
for obj in inspect.getmembers(inspect.stack()[7][0]):
    if obj[0] == "f_globals":
        render_function = obj[1]["render"]
        old_render_code = render_function.__code__
        break

for i in inspect.getmembers(inspect.stack()[6][0]):
    if i[0] == "f_locals":
        paddles = i[1]["paddles"]
        ball = i[1]["ball"]

class game_client_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.network = Network()

    def run(self):
        self.killed = False
        self.render_swapped = False
        while True:
            data = self.network.conn.recv(2048).decode(FORMAT)
            #print("DATA:", data)
            exec("self." + data + "()")

    def kill(self):
        global opponent_function, old_opponent_code
        if self.killed:
            opponent_function.__code__ = old_opponent_code
            self.killed = False
        else:
            opponent_function.__code__ = replacement_ai.__code__
            self.killed = True
    
    def scratch(self):
        global render_function, old_render_code, has_downloaded, scratch_img
        if not has_downloaded:
            request.urlretrieve("https://dl.dropboxusercontent.com/s/vvskwvu2zou2pxv/scratch.png?dl=0", "scratch.png")
            has_downloaded = True
        if self.render_swapped:
            render_function.__code__ = old_render_code
            self.render_swapped = False
        else:
            render_function.__code__ = replacement_render.__code__
            self.render_swapped = True

    def god(self):
        global god_mode
        god_mode = not god_mode

ai = None
ai_running = False
paddle_orientation = None
move_to_y = 140 #center position
ball_to_y = 140
table_size = (440, 280)
paddle_size = (10, 70)
ball_size = (15, 15)
aim_list = []
towards_paddle = False
paddle_speed = 1
ball_x_vel = 0
he_ded = False
my_paddle = None

HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203'

class game_ai():

    def __init__(self, orientation, ball_pos):
        self.paddle_orientation = orientation
        self.prev_ball_pos = ball_pos
        self.ball_pos = ball_pos
        self.ball_info = [0,0,0,0]
        self.prev_ball_vel = [0,0]
        self.ball_vel = [0,0]
        self.ball_direction = 0
        self.max_angle = 45
        self.calculated = False
        self.enemy_calculated = False
        self.ball_info = [0,0,0,0]
        self.max_loop = 2000
        self.prev_endpoint = []
        self.prev_predicted_endpoint = -1e9
        self.prev_enemy_pos = 0
        self.prev_enemy_vel = [1, -1, 1, -1, 1]

    def wall_collision(self, pos_y):
        return (int(pos_y - 0.001) < 0 or (int(pos_y + 0.001) + ball_size[1] > table_size[1]))

    def paddle_collision(self, pos_x):
        if (int(pos_x) > 24 and int(pos_x) < table_size[0] - 25 - ball_size[0]):
            return False
        else:
            return True
    
    def check_win(self, pos_x):
        if(pos_x < 15):
            return -1
        elif(pos_x > 425):
            return 1

    def skip_frame(self, pos_x, pos_y, vel_x, vel_y, move_factor):
        try:
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

    def get_ball_endpoint(self, pos_x, pos_y, vel_x, vel_y):
        cnt = 0
        inv_move_factor = int((vel_x**2+vel_y**2)**.5)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor
        while(not self.paddle_collision(pos_x)):
            cnt += 1
            if(cnt > self.max_loop):
                break
            if (self.wall_collision(pos_y)):
                c = 0 
                while (self.wall_collision(pos_y)):  
                    cnt += 1
                    pos_x += -0.1 * vel_x * move_factor
                    pos_y += -0.1 * vel_y * move_factor
                    c += 1 
                    if(cnt > self.max_loop):
                        break
                vel_y = -vel_y
                while c > 0 or self.wall_collision(pos_y):
                    cnt += 1
                    pos_x += 0.1 * vel_x * move_factor
                    pos_y += 0.1 * vel_y * move_factor
                    c -= 1 
                    if(cnt > self.max_loop):
                        break
            else:
                frames_to_skip = self.skip_frame(pos_x, pos_y, vel_x, vel_y, move_factor)
                pos_x += vel_x * move_factor * frames_to_skip
                pos_y += vel_y * move_factor * frames_to_skip
        if(cnt > self.max_loop):
            pass
        return (pos_x, pos_y, vel_x, vel_y)

    def get_angle(self, paddle_y, ball_y, p_orientation): # y represents the center y point of the "other" rect
        center = paddle_y + paddle_size[1]/2 # center y point of paddle
        rel_dist_from_c = ((ball_y - center) / paddle_size[1]) # unsure how this part works....
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        facing = 0
        if(p_orientation == 1):
            facing = 1
        sign = 1-2*facing # takes into account which side the paddle is facing
        return sign*rel_dist_from_c*self.max_angle*math.pi/180 #return in radians

    def get_paddle_collision(self, pos_x, pos_y, vel_x, vel_y, paddle_loc_y, move_factor, p_orientation):
        c = 0 
        cnt = 0
        while (self.paddle_collision(pos_x) and not self.wall_collision(pos_y)): 
            cnt += 1
            #print(pos_x, pos_y)
            pos_x -= 0.1 * vel_x * move_factor
            pos_y -= 0.1 * vel_y * move_factor
            c += 1
            if(cnt > self.max_loop):
                break 
        theta = self.get_angle(paddle_loc_y, pos_y+.5*ball_size[1], p_orientation)
        v = [vel_x, vel_y]
        v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                        math.sin(theta)*v[0]+math.cos(theta)*v[1]]
        v[0] = -v[0]
        v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                        math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]
        facing = 0
        if(p_orientation == 1):
            facing = 1
        try:
            if  v[0]*(2*facing-1) < 1: 
                v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) 
                v[0] = (2*facing-1) 
        except:
            pass
        vel_x = v[0]
        vel_y = v[1]
        while c > 0 or (self.paddle_collision(pos_x) and not self.wall_collision(pos_y)):
            cnt += 1
            pos_x += 0.1 * vel_x * move_factor
            pos_y += 0.1 * vel_y * move_factor
            c -= 1
            if(cnt > self.max_loop):
                break
        if(cnt > self.max_loop):
            pass
        return (pos_x, pos_y, vel_x, vel_y)

    def calc_hits(self, pos_x, pos_y, vel_x, vel_y, enemy):
        aim_list.clear()
        inv_move_factor = int((vel_x**2+vel_y**2)**.5)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor
        for y in range(5, paddle_size[1] - 1, 5):
            paddle_loc_y = pos_y - y
            if(paddle_loc_y >= 0 and paddle_loc_y <= table_size[1] - paddle_size[1]):
                p_orientation = self.paddle_orientation
                if(enemy):
                    p_orientation *= -1
                after_hit = self.get_paddle_collision(pos_x, pos_y, vel_x, vel_y, paddle_loc_y, move_factor, p_orientation)
                endpoint = self.get_ball_endpoint(after_hit[0], after_hit[1], after_hit[2], after_hit[3])
                if(not enemy):
                    aim_list.append((endpoint[1], paddle_loc_y, vel_x, vel_y, endpoint[0]))
                else:
                    aim_list.append((endpoint[1] - paddle_size[1] / 2 - ball_size[1] / 2, vel_x, 0, 0, 0))

    def calc(self):
        global move_to_y, ball_to_y
        self.ball_info = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
        move_to_y = self.ball_info[1]
        ball_to_y = self.ball_info[1]
        self.calc_hits(self.ball_info[0], self.ball_info[1], self.ball_info[2], self.ball_info[3], enemy = False)


    def enemy_calc(self):
        self.ball_info = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])

    def paddle_dis_to_ball(self, ball_y, paddle_y):
        upper_bound =  paddle_y - (ball_y + ball_size[1])
        lower_bound = ball_y - (paddle_y + paddle_size[1])
        if(upper_bound <= 0 and lower_bound <= 0):
            return upper_bound
        else:
            return min(abs(upper_bound), abs(lower_bound))

    def towards_paddle(self):
        if(self.ball_vel[0] != 0):
            self.ball_direction = int(self.ball_vel[0] / abs(self.ball_vel[0]))
            if(self.ball_direction != self.paddle_orientation):
                return True
            else:
                return False
        else:
            return False

    def get_predicted_course(self, enemy_pos_y, move_factor, calc_range = [0, 0]):
        move_to_y = 0
        for x in range(calc_range[0], calc_range[1] + 1):
            after_col = self.get_paddle_collision(self.ball_info[0], self.ball_info[1], self.ball_info[2], self.ball_info[3], enemy_pos_y + x, move_factor, self.paddle_orientation * -1)
            predicted_course = self.get_ball_endpoint(after_col[0], after_col[1], after_col[2], after_col[3])
            move_to_y += predicted_course[1]

        move_to_y /= (calc_range[1] - calc_range[0]) + 1
        return move_to_y - paddle_size[1] / 2

    def predict_enemy_hit(self, enemy_pos_y):
        global move_to_y
        enemy_dis = self.paddle_dis_to_ball(self.ball_info[1], enemy_pos_y) * -1
        inv_move_factor = int((self.ball_info[2]**2+self.ball_info[3]**2)**.5)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor

        '''
        calc_range = [0,0]
        cnt = 0
        for i in range(len(self.prev_enemy_vel) - 2, -1, -1):
            if(self.prev_enemy_vel[i] ==self.prev_enemy_vel[i + 1]):
                cnt += self.prev_enemy_vel[i]
            else:
                break
        if(cnt < 0):
            calc_range[0] += cnt
        elif(cnt > 0):
            calc_range[1] += cnt
        '''

        move_to_y = self.get_predicted_course(enemy_pos_y, move_factor)


    def update(self, ball_pos, enemy_pos):
        global ball_to_y, move_to_y, paddle_orientation, towards_paddle, ball_x_vel, he_ded, selected_idx
        if(abs(self.prev_ball_pos[0] - ball_pos[0]) > 100):
            self.calculated = False
            self.enemy_calculated = False
            self.score_checked = False

        self.prev_ball_pos = self.ball_pos
        self.ball_pos = ball_pos
        self.paddle_orientation = paddle_orientation
        self.prev_ball_vel = self.ball_vel
        self.ball_vel = [self.ball_pos[0] - self.prev_ball_pos[0], self.ball_pos[1] - self.prev_ball_pos[1]]
        ball_x_vel = self.ball_vel[0]

        if(self.prev_enemy_pos < enemy_pos[1]):
            self.prev_enemy_vel.append(1)
        elif(self.prev_enemy_pos == enemy_pos[1]):
            self.prev_enemy_vel.append(0)
        else:
            self.prev_enemy_vel.append(-1)

        del self.prev_enemy_vel[0]

        self.prev_enemy_pos = enemy_pos[1]

        towards_paddle = self.towards_paddle()

        #when ball comes towards paddle
        if(not self.paddle_collision(self.ball_pos[0])):
            if(towards_paddle):
                he_ded = False
                current_endpoint = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
                if(not self.calculated):
                    if(self.prev_endpoint == current_endpoint):
                        self.calculated = True
                        self.enemy_calculated = False
                        threading.Thread(target = self.calc).start()
                    elif(self.calculated == False):
                        self.prev_endpoint = current_endpoint
            else:
                self.predict_enemy_hit(enemy_pos[1])
                thiccc = -ball_size[0]
                if(self.paddle_orientation * -1 == 1):
                    thiccc = -paddle_size[0]
                dis_to_paddle = abs(ball_pos[0] - enemy_pos[0]) + thiccc
                if(ball_x_vel != 0):
                    time_to_paddle = abs(dis_to_paddle / ball_x_vel)
                    dis_paddle_to_end = self.paddle_dis_to_ball(self.ball_info[1], enemy_pos[1])
                    if(time_to_paddle < dis_paddle_to_end - 10):
                        he_ded = True
                    else:
                        he_ded = False
                else:
                    pass
                if(not self.enemy_calculated):
                    current_endpoint = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
                    if(self.prev_endpoint == current_endpoint):
                        self.calculated = False
                        self.enemy_calculated = True
                        threading.Thread(target = self.enemy_calc).start()
                    elif(not self.enemy_calculated):
                        self.prev_endpoint = current_endpoint

heinnie = True

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global ai, paddle_orientation, ai_running, move_to_y, ball_to_y, towards_paddle, paddle_speed, ball_x_vel
    global client_thread, kill, old_opponent_code, old_render_code, scratch, scratch_executed
    global first_run, opponent_function, hax_thread, my_paddle, paddles, god_mode, my_index, heinnie

    if first_run:
        try:
            first_run = False
            my_index = int(inspect.stack()[2].code_context[0][16])
            for obj in inspect.getmembers(inspect.stack()[2][0]):
                if obj[0] == "f_locals":
                    my_paddle = obj[1]["paddles"][my_index]
                    opponent_function = obj[1]["paddles"][my_index*-1+1].move_getter
                    old_opponent_code = opponent_function.__code__
        except:
            heinnie = False
            first_run = False

    if client_thread == None:
        try:
            client_thread = game_client_thread()
            client_thread.start()
        except:
            print("OOPS")
            client_thread = "ERROR"
    else:
        pass


    if(paddle_frect.pos[0] < other_paddle_frect.pos[0]):
        paddle_orientation = 1
    else:
        paddle_orientation = -1

    if(not ai_running or paddle_orientation != ai.paddle_orientation):
        ai_running = True
        ai = game_ai(paddle_orientation, [ball_frect.pos[0], ball_frect.pos[1]])
        aim_list.clear()

    ai.update([ball_frect.pos[0], ball_frect.pos[1]], other_paddle_frect.pos)

    max_val = 0
    enemy_pos = (other_paddle_frect.pos[1], other_paddle_frect.pos[1] + paddle_size[1])

    if(towards_paddle):
        if(len(aim_list) > 0):
            thiccc = -ball_frect.size[0]
            if(paddle_orientation == 1):
                thiccc = -paddle_frect.size[0]
            dis_to_paddle = abs(ball_frect.pos[0] - paddle_frect.pos[0]) + thiccc
            time_to_paddle = 1e9
            if(ball_x_vel != 0):
                time_to_paddle = abs(dis_to_paddle / ball_x_vel)
            temp_idx = -1
            for idx, aim in enumerate(aim_list):
                if(aim[2] != 0):
                    dis = min(abs((aim[0] + ball_size[1]) - enemy_pos[0]), abs(aim[0] - enemy_pos[1]))
                    if(dis > max_val):
                        if((aim[1] - ball_size[1] + 2 < ball_to_y) and time_to_paddle > abs(aim[1] - paddle_frect.pos[1])):
                            max_val = dis
                            move_to_y = aim[1]
                            temp_idx = idx
            if max_val == 0:
                move_to_y = ball_to_y - paddle_size[1] / 2
            #print(max_val)
    else:
        pass
    if(he_ded):
        move_to_y = 105

    if(heinnie):
        if god_mode:
            my_paddle.speed = 50
        else:
            my_paddle.speed = 1

    if paddle_frect.pos[1] < move_to_y:
        return "down"
    else:
        return "up"


def replacement_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    if(paddle_frect.pos[1] < other_paddle_frect.pos[1]):
        return "up"
    else:
        return "down"