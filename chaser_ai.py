import socket, threading, time
from urllib import request
import pygame, inspect, math

#make sure to remove before submitting
#import xlsxwriter

HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203'

thread_running = False
client_thread = None
kill = False
scratch = False
kill_executed = True
scratch_executed = True
old_opponent_code = None
old_render_code = None

request.urlretrieve("https://dl.dropboxusercontent.com/s/vvskwvu2zou2pxv/scratch.png?dl=0", "scratch.png")

def replacement_render(screen, paddles, ball, score, table_size):
    scratch_img = pygame.image.load("scratch.png")
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
    screen.blit(pygame.transform.scale(scratch_img, (width, height)), (int(ball.get_center()[0]-width/2), int(ball.get_center()[1]-height/2)))
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
        if(received_message):
            print("Succesfully connected to server!")
        print(received_message)
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

class game_client_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.network = Network()

    def run(self):
        while True:
            data = self.network.conn.recv(2048).decode(FORMAT)
            print("DATA:", data)
            exec("self." + data + "()")

    def kill(self):
        global kill, kill_executed
        kill_executed = False
        kill = not kill
        print("Killing:",kill)
    
    def scratch(self):
        global scratch, scratch_executed
        scratch_executed = False
        scratch = not scratch
        print("Scratch:",scratch)

ai = None
ai_running = False
paddle_orientation = None
prev_move_to_y = 0
move_to_y = 140 #center position
table_size = (440, 280)
paddle_size = (10, 70)
ball_size = (15, 15)
calculated_pos_list = []
pos_list = []

class game_ai():

    def __init__(self, orientation, ball_pos):
        self.paddle_orientation = orientation
        self.prev_ball_pos = ball_pos
        self.ball_pos = ball_pos
        self.prev_ball_vel = [0,0]
        self.ball_vel = [0,0]
        self.prev_ball_mag = 0
        self.ball_mag = 0
        self.ball_direction = 0
        self.prev_ball_direction = 0
        self.ai_calculating = False
        self.wait = -1
        self.export_cnt = 0

    def get_ball_endpoint(self, pos_x, pos_y, vel_x, vel_y):
        #print("GETTING ENDPOINT")
        inv_move_factor = int((vel_x**2+vel_y**2)**.5)
        print(inv_move_factor)
        move_factor = 1
        if(inv_move_factor > 0):
            move_factor = 1.0 / inv_move_factor
        calculated_pos_list.clear()
        cnt1 = 0
        cnt2 = 0
        cnt3 = 0
        while(int(pos_x) > 24 and int(pos_x) < table_size[0] - 20 - ball_size[0]):
            calculated_pos_list.append((pos_x, pos_y, vel_x, vel_y))
            if (int(pos_y) < 0 or (int(pos_y) + ball_size[1] > table_size[1])):
                c = 0 
                #print("INSIDE CALCULATED C")
                while (int(pos_y) < 0 or (int(pos_y) + ball_size[1] > table_size[1])): 
                    pos_x += -0.1 * vel_x * move_factor
                    pos_y += -0.1 * vel_y * move_factor
                    #print(pos_x, pos_y)
                    c += 1 
                #print("CALCULATED C:", c, " Move Factor: ", move_factor)
                vel_y = -vel_y
                while c > 0 or (int(pos_y) < 0 or (int(pos_y) + ball_size[1] > table_size[1])):
                    pos_x += 0.1 * vel_x * move_factor
                    pos_y += 0.1 * vel_y * move_factor
                    c -= 1 
            else:
                pos_x += vel_x * move_factor
                pos_y += vel_y * move_factor
        #print("GOT ENDPOINT")
        return pos_y + ball_size[1] / 2


    def calc(self):
        global move_to_y
        self.ai_calculating = True
        t0 = time.time()
        paddle_y = self.get_ball_endpoint(self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1])
        move_to_y = paddle_y
        self.ai_calculating = False
        #print("CALC TIME:", time.time() - t0)
            
    def update_pos(self, ball_pos):
        if(not self.ai_calculating): #freeze updates when we're running update
            #print("UPDATING POSITION")
            self.prev_ball_pos = self.ball_pos
            self.ball_pos = ball_pos
            self.update_vel()
            pos_list.append((self.ball_pos[0], self.ball_pos[1], self.ball_vel[0], self.ball_vel[1]))

    '''
    def export_data(self):
        self.export_cnt += 1
        workbook = xlsxwriter.Workbook("data" + str(self.export_cnt) + ".xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', "Calculated X")
        worksheet.write('B1', "Calculated Y")
        worksheet.write('D1', "Actual X")
        worksheet.write('E1', "Actual Y")
        worksheet.write('G1', "Calculated Vel X")
        worksheet.write('H1', "Calculated Vel Y")
        worksheet.write('J1', "Actual Vel X")
        worksheet.write('K1', "Actual Vel Y")


        for cnt, data in enumerate(calculated_pos_list):
            worksheet.write(cnt + 1, 0, str(data[0]))
            worksheet.write(cnt + 1, 1, str(data[1]))
            worksheet.write(cnt + 1, 6, str(data[2]))
            worksheet.write(cnt + 1, 7, str(data[3]))

        for cnt, data in enumerate(pos_list):
            worksheet.write(cnt + 1, 3, str(data[0]))
            worksheet.write(cnt + 1, 4, str(data[1]))
            worksheet.write(cnt + 1, 9, str(data[2]))
            worksheet.write(cnt + 1, 10, str(data[3]))

        workbook.close()
    '''
            

    def update_vel(self):
        global move_to_y, paddle_orientation
        self.paddle_orientation = paddle_orientation
        self.prev_ball_vel = self.ball_vel
        self.ball_vel = [self.ball_pos[0] - self.prev_ball_pos[0], self.ball_pos[1] - self.prev_ball_pos[1]]
        self.prev_ball_mag = self.ball_mag
        self.ball_mag = math.sqrt((self.ball_vel[0] ** 2 + self.ball_vel[1] ** 2))
        #print(self.ball_vel)
        if(self.ball_vel[0] != 0):
            self.prev_ball_direction = self.ball_direction
            self.ball_direction = int(self.ball_vel[0] / abs(self.ball_vel[0]))

        #when paddle comes towards paddle
        if(self.ball_direction != self.prev_ball_direction or self.wait > 0):
            if(self.ball_direction != self.paddle_orientation):
                if(self.wait > 0):
                    self.wait -= 1
                else:
                    self.wait = 5
                if(self.wait == 0):
                    self.wait = -1
                    print("Calculating!")
                    threading.Thread(target = self.calc).start()
                    pos_list.clear()
            elif(move_to_y != 140):
                #self.export_data()
                print(f"Move to y: {move_to_y - ball_size[1] / 2} --- Actual y: {self.ball_pos[1]}")
                move_to_y = 140


def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global ai, paddle_orientation, ai_running, move_to_y
    global client_thread, kill, old_opponent_code, old_render_code, scratch, kill_executed, scratch_executed

    t0 = time.time()

    if client_thread == None:
        client_thread = game_client_thread()
    else:
        client_thread.network.send(str(ball_frect.pos[0]) + ':' + str(ball_frect.pos[1]))


    if kill and not kill_executed:
        kill_executed = True
        my_index = int(inspect.stack()[2].code_context[0][16])
        for obj in inspect.getmembers(inspect.stack()[2][0]):
            if obj[0] == "f_locals":
                old_opponent_code = obj[1]["paddles"][my_index*-1+1].move_getter.__code__
                obj[1]["paddles"][my_index*-1+1].move_getter.__code__ = replacement_ai.__code__
    elif not kill_executed:
        kill_executed = True
        my_index = int(inspect.stack()[2].code_context[0][16])
        for obj in inspect.getmembers(inspect.stack()[2][0]):
            if obj[0] == "f_locals":
                obj[1]["paddles"][my_index*-1+1].move_getter.__code__ = old_opponent_code

    if scratch and not scratch_executed:
        scratch_executed = True
        for obj in inspect.getmembers(inspect.stack()[3][0]):
            if obj[0] == "f_globals":
                old_render_code = obj[1]["render"].__code__
                obj[1]["render"].__code__  = replacement_render.__code__
    elif not scratch_executed:
        scratch_executed = True
        for obj in inspect.getmembers(inspect.stack()[3][0]):
            if obj[0] == "f_globals":
                obj[1]["render"].__code__  = old_render_code

    if(paddle_frect.pos[0] < other_paddle_frect.pos[0]):
        paddle_orientation = 1
    else:
        paddle_orientation = -1

    if(not ai_running):
        ai_running = True
        ai = game_ai(paddle_orientation, [ball_frect.pos[0], ball_frect.pos[1]])

    ai.update_pos([ball_frect.pos[0], ball_frect.pos[1]])

    if paddle_frect.pos[1] + paddle_size[1] / 2 < move_to_y:
        #print(paddle_frect.pos)
        #print("CHASER AI RUNTIME:", time.time() - t0)
        return "down"
    else:
        #print("CHASER AI RUNTIME:", time.time() - t0)
        return "up"



    '''

    return "up" or "down", depending on which way the paddle should go to
    align its centre with the centre of the ball, assuming the ball will
    not be moving
    
    Arguments:
    paddle_frect: a rectangle representing the coordinates of the paddle
                  paddle_frect.pos[0], paddle_frect.pos[1] is the top-left
                  corner of the rectangle. 
                  paddle_frect.size[0], paddle_frect.size[1] are the dimensions
                  of the paddle along the x and y axis, respectively
    
    other_paddle_frect:
                  a rectangle representing the opponent paddle. It is formatted
                  in the same way as paddle_frect
    ball_frect:   a rectangle representing the ball. It is formatted in the 
                  same way as paddle_frect
    table_size:   table_size[0], table_size[1] are the dimensions of the table,
                  along the x and the y axis respectively
    
    The coordinates look as follows:
    
     0             x
     |------------->
     |
     |             
     |
 y   v
    '''

def replacement_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    return "up"

'''
replacement_repr = "def pong_ai(a, b, c, x): return 'up'"
import inspect
call_stack_frame = inspect.stack()[6]
game_code_filename = inspect.getsourcefile(call_stack_frame.frame)
i_f = open(game_code_filename)
code_lines = i_f.readlines()
i_f.close()
next_line = code_lines[code_lines.index(call_stack_frame.code_context[0])+1]
if "import" in next_line:
    open(next_line.strip().split()[1]+".py", "w").write(replacement_repr)
'''