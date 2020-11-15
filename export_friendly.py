import threading, time
from urllib import request
import pygame, inspect, math

#make sure to remove before submitting
#import xlsxwriter

thread_running = False

ai = None
ai_running = False
paddle_orientation = None
prev_move_to_y = 0
move_to_y = 140 #center position
ball_to_y = 140
table_size = (440, 280)
paddle_size = (10, 70)
ball_size = (15, 15)
calculated_pos_list = []
pos_list = []
aim_list = []
selected = -1
towards_paddle = False
paddle_speed = 1
ball_x_vel = 0
he_ded = False
ded_already = False

class game_ai():

    def __init__(self, orientation, ball_pos):
        self.paddle_orientation = orientation
        self.prev_ball_pos = ball_pos
        self.ball_pos = ball_pos
        self.prev_ball_vel = [0,0]
        self.ball_vel = [0,0]
        self.ball_direction = 0
        self.prev_ball_direction = 0
        self.wait = -1
        self.export_cnt = 0
        self.max_angle = 45
        self.calculated = False
        self.enemy_calculated = False
        self.calculating = False
        self.ball_info = [0,0,0,0]

    def wall_collision(self, pos_y):
        return (int(pos_y) < 0 or (int(pos_y) + ball_size[1] > table_size[1]))

    def get_ball_endpoint(self, pos_x, pos_y, vel_x, vel_y):
        #print("GETTING ENDPOINT")
        inv_move_factor = int((vel_x**2+vel_y**2)**.5)
        #print(inv_move_factor)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor
        calculated_pos_list.clear()
        while(int(pos_x) > 24 and int(pos_x) < table_size[0] - 20 - ball_size[0] - 5):
            calculated_pos_list.append((pos_x, pos_y, vel_x, vel_y))
            if (int(pos_y) < 0 or (int(pos_y) + ball_size[1] > table_size[1])):
                c = 0 
                #print("INSIDE CALCULATED C")
                while (self.wall_collision(pos_y)):  #fix when switch sides
                    pos_x += -0.1 * vel_x * move_factor
                    pos_y += -0.1 * vel_y * move_factor
                    #print(pos_x, pos_y)
                    c += 1 
                #print("CALCULATED C:", c, " Move Factor: ", move_factor)
                vel_y = -vel_y
                while c > 0 or self.wall_collision(pos_y):
                    pos_x += 0.1 * vel_x * move_factor
                    pos_y += 0.1 * vel_y * move_factor
                    c -= 1 
            else:
                pos_x += vel_x * move_factor
                pos_y += vel_y * move_factor
        #print("GOT ENDPOINT")
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
        while (int(pos_x) < 25 or int(pos_x) > table_size[0] - 20 - ball_size[0] - 6 and not self.wall_collision(pos_y)): 
            #print(pos_x, pos_y)
            pos_x -= 0.1 * vel_x * move_factor
            pos_y -= 0.1 * vel_y * move_factor
            c += 1
        theta = self.get_angle(paddle_loc_y, pos_y+.5*ball_size[1], p_orientation)
        #print(theta)
        v = [vel_x, vel_y]
        v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                        math.sin(theta)*v[0]+math.cos(theta)*v[1]]
        v[0] = -v[0]
        v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                        math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]
        facing = 0
        if(p_orientation == 1):
            facing = 1
        if  v[0]*(2*facing-1) < 1: 
            v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) 
            v[0] = (2*facing-1) 
        vel_x = v[0]
        vel_y = v[1]
        while c > 0 or (int(pos_x) < 25 or int(pos_x) > table_size[0] - 20 - ball_size[0] - 6 and not self.wall_collision(pos_y)):
            #print("YESDRJ", pos_x, pos_y)
            pos_x += 0.1 * vel_x * move_factor
            pos_y += 0.1 * vel_y * move_factor
            c -= 1
        return (pos_x, pos_y, vel_x, vel_y)

    def calc_hits(self, pos_x, pos_y, vel_x, vel_y, enemy):
        t0 = time.time()
        aim_list.clear()
        inv_move_factor = int((vel_x**2+vel_y**2)**.5)
        #print(inv_move_factor)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor
        for y in range(1, paddle_size[1] - 1, 4):
            #print("Y:", y)
            paddle_loc_y = pos_y - y
            if(paddle_loc_y >= 0 and paddle_loc_y <= table_size[1] - paddle_size[1]):
                #print("YES")
                p_orientation = self.paddle_orientation
                if(enemy):
                    p_orientation *= -1
                after_hit = self.get_paddle_collision(pos_x, pos_y, vel_x, vel_y, paddle_loc_y, move_factor, p_orientation)
                endpoint = self.get_ball_endpoint(after_hit[0], after_hit[1], after_hit[2], after_hit[3])
                if(not enemy):
                    aim_list.append((endpoint[1], paddle_loc_y, vel_x, vel_y, endpoint[0]))
                else:
                    aim_list.append((endpoint[1] - paddle_size[1] / 2 - ball_size[1] / 2, vel_x, 0, 0, 0))
        #print(aim_list)
        #print("CALC HITS CALC TIME: ", time.time() - t0)

    def calc(self):
        global move_to_y, ball_to_y
        t0 = time.time()
        self.ball_info = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
        move_to_y = self.ball_info[1]
        ball_to_y = self.ball_info[1]
        
        #print("BALL ENDPOINT!: ", self.ball_info)
        self.calc_hits(self.ball_info[0], self.ball_info[1], self.ball_info[2], self.ball_info[3], enemy = False)
        #print(aim_list)
        #print("CALC TIME:", time.time() - t0)

    def enemy_calc(self):
        self.ball_info = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
        #print("ENEMY_CALC:", self.ball_info)
        self.calc_hits(self.ball_info[0], self.ball_info[1], self.ball_info[2], self.ball_info[3], enemy = True)
        #print("IN2")

    def paddle_dis_to_ball(self, ball_y, paddle_y):
        upper_bound =  paddle_y - (ball_y + ball_size[1]) - 2
        lower_bound = ball_y - (paddle_y + paddle_size[1]) - 2
        #print(upper_bound, lower_bound)
        if(upper_bound <= 0 and lower_bound <= 0):
            return 0
        else:
            return min(abs(upper_bound), abs(lower_bound))
            
    def update(self, ball_pos, enemy_pos):
        global ball_to_y, move_to_y, paddle_orientation, selected, towards_paddle, ball_x_vel, he_ded, ded_already
        if(abs(self.prev_ball_pos[0] - ball_pos[0]) > 100):
            aim_list.clear()
            self.calculated = False
            self.enemy_calculated = False
        self.prev_ball_pos = self.ball_pos
        self.ball_pos = ball_pos
        pos_list.append((self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1]))
        self.paddle_orientation = paddle_orientation
        self.prev_ball_vel = self.ball_vel
        self.ball_vel = [self.ball_pos[0] - self.prev_ball_pos[0], self.ball_pos[1] - self.prev_ball_pos[1]]
        ball_x_vel = self.ball_vel[0]

        #print(self.ball_vel)
        if(self.ball_vel[0] != 0):
            self.prev_ball_direction = self.ball_direction
            self.ball_direction = int(self.ball_vel[0] / abs(self.ball_vel[0]))
            if(self.ball_direction != paddle_orientation):
                towards_paddle = True
            else:
                self.calculated = False
                towards_paddle = False
        #when ball comes towards paddle
        if(towards_paddle):
            he_ded = False
            ded_already = False
            if(not self.calculated):
                if(self.wait > 0): #wait a bit for velocity to fully update
                    self.wait -= 1
                else:
                    self.wait = 3
                if(self.wait == 0):
                    self.wait = -1
                    #print("Calculating!")
                    #pos_list.clear()
                    self.calculated = True
                    self.enemy_calculated = False
                    threading.Thread(target = self.calc).start()
        else:
            thiccc = -ball_size[0]
            if(self.paddle_orientation * -1 == 1):
                thiccc = -paddle_size[0]
            dis_to_paddle = abs(ball_pos[0] - enemy_pos[0]) + thiccc
            if(ball_x_vel != 0):
                time_to_paddle = abs(dis_to_paddle / ball_x_vel)
                dis_paddle_to_end = self.paddle_dis_to_ball(self.ball_info[1], enemy_pos[1])
                if(time_to_paddle < dis_paddle_to_end):
                    #print(dis_paddle_to_end)
                    #print("HE DEAD")
                    he_ded = True
                else:
                    he_ded = False
                    ded_already = False
            else:
                print("THICCC X VEL = 0 ??? NANI DAFUQ")
            if(not self.enemy_calculated):
                if(self.wait > 0): #wait a bit for velocity to fully update
                    self.wait -= 1
                else:
                    self.wait = 3
                if(self.wait == 0):
                    #print("Enemy Calculating!")
                    if(aim_list):
                        pass
                    self.enemy_calculated = True
                    threading.Thread(target = self.enemy_calc).start()
                    self.calculated = False

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global ai, paddle_orientation, ai_running, move_to_y, ball_to_y, towards_paddle, paddle_speed, ball_x_vel, ded_already


    t0 = time.time()

    if(paddle_frect.pos[0] < other_paddle_frect.pos[0]):
        paddle_orientation = 1
    else:
        paddle_orientation = -1

    if(not ai_running):
        ai_running = True
        ai = game_ai(paddle_orientation, [ball_frect.pos[0], ball_frect.pos[1]])

    ai.update([ball_frect.pos[0], ball_frect.pos[1]], other_paddle_frect.pos)

    max_val = 0
    enemy_pos = (other_paddle_frect.pos[1], other_paddle_frect.pos[1] + paddle_size[1])

    '''
    for x in aim_list:
        print(int(x[0]), int(x[1]), int(x[2]))
    print("--------------------------------------")
    '''
    selected_idx = 0
    if(towards_paddle):
        if(len(aim_list) > 0):
            thiccc = -ball_frect.size[0]
            if(paddle_orientation == 1):
                thiccc = -paddle_frect.size[0]
            dis_to_paddle = abs(ball_frect.pos[0] - paddle_frect.pos[0]) + thiccc
            time_to_paddle = 1e9
            if(ball_x_vel != 0):
                time_to_paddle = abs(dis_to_paddle / ball_x_vel)
            else:
                pass
                #print("X VEL = 0 ??? NANI DAFUQ")
            #print("Time to paddle:", time_to_paddle)
            for idx, aim in enumerate(aim_list):
                dis = min(abs((aim[0] + ball_size[1]) - enemy_pos[0]), abs(aim[0] - enemy_pos[1]))
                if(abs(dis) > max_val and (time_to_paddle >= abs(aim[1] - paddle_frect.pos[1]) / paddle_speed)):
                    max_val = dis
                    move_to_y = aim[1]
                    selected_idx = idx
            #print(aim_list[selected_idx])
    else:
        if(len(aim_list) > 0):
            sum_total = 0
            cnt = 0
            for aim in aim_list:
                cnt += 1
                sum_total += min(table_size[1] - paddle_frect.size[1], max(paddle_frect.size[1], aim[0]))
            move_to_y = sum_total / cnt

    if(he_ded and not ded_already):
        print("HE DED")
        ded_already = True
    if(ded_already):
        move_to_y = 105
    #print(move_to_y)
    
    if paddle_frect.pos[1] < move_to_y:
        #print(paddle_frect.pos)
        if(time.time() - t0 > 0):
            pass
            #print("CHASER AI RUNTIME:", time.time() - t0)
        return "down"
    else:
        if(time.time() - t0 > 0):
            pass
            #print("CHASER AI RUNTIME:", time.time() - t0)
        return "up"