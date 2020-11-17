from datetime import datetime
import socket, sys, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5050
SERVER = ''
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

    def __init__(self, threadID, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):
        while True:
            try:
                data = self.conn.recv(2048).decode(FORMAT)
                #print(data)
            except:
                print("AN ERROR HAS OCCURED!")
                break

    def kill(self):
        try:
            self.conn.send(str.encode("kill"))
            print("he ded")
        except:
            print("Could not kill :(")

    def scratch_cat_intensifies(self):
        try:
            self.conn.send(str.encode("scratch"))
            #print(self.conn.recv(2048).decode())
            print("meow")
        except:
            print("could not scratch :(")

    def god(self):
        try:
            self.conn.send(str.encode("god"))
            print("GOD INTENSIFIES")
        except:
            print("NO GOD")

    def sleep(self):
        pass

class Controller_Client_Thread(threading.Thread):

    def __init__(self, threadID, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):
        while(True):
            data = self.conn.recv(2048).decode(FORMAT).split(':')
            print(data)
            #f represents that we want to perform a function on the clients
            if(data[0] == 'f'):
                for client in game_clients:
                    if(data[1] == 'kill'):
                        self.conn.send(str.encode(str(client.kill())))
                    if(data[1] == 'scratch'):
                        self.conn.send(str.encode(str(client.scratch_cat_intensifies())))

thread_cnt = 1

while True:
    conn, addr = s.accept()
    print(f"Connection with {addr} established!")
    client_type = conn.recv(2048).decode(FORMAT)
    conn.send(str.encode(str(thread_cnt)))
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



