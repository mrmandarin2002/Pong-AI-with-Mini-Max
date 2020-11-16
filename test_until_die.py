import socket, threading, json, time, contextlib, io
from random import randint

gomoku = __import__("jessy_gomoku") #put your filename here (pls for the love of god run this shit in the same folder as your file (and for the love of jesus do not pyzo this))

HEADER = 16
PORT = 5555
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203' #hey those trying to hack my server! there ain't shit on there so gl + my gomoku server is run within a try statement so good f****** luck trying to break that shit
DELAY = 0.5 # To avoid DDos-ing MrMandarin's Server, please don't reduce the delay!

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST_IP 
        self.addr = (self.host, PORT)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        self.client.send(str.encode('controller'))
        received_message = self.client.recv(2048).decode(FORMAT)
        print(received_message)

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode("a:" + str(data)))
            print("DONE")
        except socket.error as e:
            return str(e)

    def get_analysis(self, board):
        self.client.send(str.encode('A:' + json.dumps(board)))
        return self.client.recv(2048).decode(FORMAT)

class client():

    def __init__(self):
        self.network = Network()

    #this returns a randomized board, you can also make this return your own custom board to test it against my program
    def generate_random_board(self):
        board = []
        for i in range(8):
            board.append([" "]*8)
        for i in range(randint(5, 30)):
            #this below is absolutely disgusting code but just let it be, man's on a time crunch
            yeee = ('w', 'b')
            try:
                gomoku.put_seq_on_board(board, randint(0, 7), randint(0, 7), randint(-1, 1), randint(0, 1), randint(2, 5), yeee[randint(0,1)])
            except:
                i -= 1
        return board
        '''
        str_board = json.dumps(board)
        return json.loads(str_board)
        '''

    def run(self):
        yourAnalysis = []
        serverAnalysis = []
        board = None
        correct_counter = -1

        while yourAnalysis == serverAnalysis:
            correct_counter += 1
            board = self.generate_random_board()

            f = io.StringIO()
            with contextlib.redirect_stdout(f): # temporarily redirect console output to a string buffer 
                gomoku.analysis(board)
            yourAnalysis = f.getvalue().split("\n")[0:-1] # readlines() didn't work
            
            serverAnalysis = json.loads(self.network.get_analysis(board))   
            
            time.sleep(DELAY) # no DDos :)
            print("Correct:", correct_counter) # my highscore is 17023

        print("\nFound a case that doesn't work!")
        print("\nThis is the list version of the board (for copy-paste):\n", board)
        print("\nBoard:")
        gomoku.print_board(board)
        print("\nHere is the difference between the analyses:\n")

        # if analyses aren't the same length, then you messed up gomoku.analysis()
        for i in range(len(serverAnalysis)): 
            
            # which stone colour?
            if yourAnalysis[i].find("stones") >= 0:
                print(yourAnalysis[i])
            # either print only the lines that are wrong:
            if yourAnalysis[i] != serverAnalysis[i]:
                print("  Your:", yourAnalysis[i])
                print("Server:", serverAnalysis[i])
                print("")
            # or print all the lines:
            # print("Your:", myAnalysis[i])
            # print("Server:", serverAnalysis[i])
            # print("")
            
root = client()
root.run()
