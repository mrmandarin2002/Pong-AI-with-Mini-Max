from datetime import datetime
import socket, sys, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5050
SERVER = 'localhost'
FORMAT = 'utf-8'
HEADER = 2048

SERVER_IP = socket.gethostbyname(SERVER)

try:
    s.bind((SERVER, PORT))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

controller_clients = []
game_clients = []

class Game_Client_Thread(threading.Thread):

    def __init__(self, threadID, client_type, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):
        while True:
            try:
                data = self.conn.recv(2048).decode(FORMAT)
                print(data)
            except:
                print("AN ERROR HAS OCCURED!")


class Controller_Client_Thread(threading.Thread):

    def __init__(self, threadID, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):
        pass

while True:
    conn, addr = s.accept()
    print(f"Connection with {addr} established!")
    thread_cnt = 1
    client_type = conn.recv(2048).decode(FORMAT)
    conn.send(str.format(str(thread_cnt)))
    if(client_type == 'game'):
        print("Connection with game client established!")
        game_clients.append(Game_Client_Thread(thread_cnt, addr, conn))
        game_clients[len(game_clients) - 1].start()
        thread_cnt += 1
    elif(client_type == 'controller'):
        print("Connection with controller client established!")
        controller_clients.append(Controller_Client_Thread(thread_cnt, addr, conn))
        controller_clients[len(controller_clients) - 1].start()
        thread_cnt += 1
    else:
        print("IDK dafuq ur ass trying to connect with")



