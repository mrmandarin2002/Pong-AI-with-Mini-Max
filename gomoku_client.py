import socket, threading, json
from random import *
import tkinter as tk
from tkinter import *

gomoku = __import__("gomoku") #put your filename here (pls for the love of god run this shit in the same folder as your file (and for the love of jesus do not pyzo this))

HEADER = 16
PORT = 5555
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203' #hey those trying to hack my server! there ain't shit on there so gl + my gomoku server is run within a try statement so good f****** luck trying to break that shit

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

class client(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.network = Network()
        analysis = Button(self, text = "ANALYZE!", command = self.analyze)
        analysis.pack(padx = 20, pady = 10)

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

    def analyze(self):
        print("GENERATED BOARD:")
        board = self.generate_random_board()
        gomoku.print_board(board)
        print("HERE'S YOUR ANALYSIS:")
        gomoku.analysis(board)
        print("-------------------------------")
        analysis = json.loads(self.network.get_analysis(board))
        print("HERE'S MRMANDARINS ANALYSIS:")
        for a in analysis:
            print(a)
        print('\n')
        
        
BLUE = "#DFF9FB"

root = client()
root.configure(background = BLUE)
root.title("GUERZHOY IS JESUS")
root.geometry("420x69")
root.mainloop()
