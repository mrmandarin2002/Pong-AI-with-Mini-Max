import socket, threading
import tkinter as tk
from tkinter import *

HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
HOST_IP = '172.105.7.203'

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
            print("DONE")
            #print(self.client.recv(2048).decode(FORMAT))
        except socket.error as e:
            return str(e)

class client(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.network = Network()
        #client_frame = Frame(self)
        kill_button = Button(self, text = "KILL", command = lambda : self.network.send('f:kill'))
        kill_button.pack(padx = 20, pady = 10)
        scratch_button = Button(self, text = "SCRATCH", command = lambda : self.network.send('f:scratch'))
        scratch_button.pack(padx = 20, pady = 10)
        god_button = Button(self, text = "GOD MODE", command = lambda : self.network.send('f:god'))
        god_button.pack(padx = 20, pady = 10)
        #kill_button.grid(row = 0, column = 0, padx = 50, pady = 50)
        
BLUE = "#DFF9FB"

root = client()
root.configure(background = BLUE)
root.title("PONG BITCHES")
root.mainloop()
