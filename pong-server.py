from datetime import datetime
import socket, sys, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5050
SERVER = 'localhost'
FORMAT = 'utf-8'
HEADER = 2048

SERVER_IP = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

clients = []

class Game_Client_Thread(threading.Thread):

    def __init__(self, threadID, client_type, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):
        pass

class Controller_Client_Thread(threading.Thread):

    def __init__(self, threadID, client_type, addr, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client_type = client_type
        self.addr = addr
        self.conn = conn

    def run(self):


while True:
    conn, addr = s.accept()
    print(f"Connection with {addr} established!")

    thread_cnt = 1
    start_new_thread(threaded_client, (conn,))
    client_type = conn.recv(2048).decode(FORMAT)
    if(client_type == 'game'):
        check = True
        for client in clients:
            if(client.client_type == 'game'):
                print("You cannot connect two games to the server")
                check = False
        if(check):
            clients.append(Game_Client_Thread(thread_cnt, 'game', addr, conn))
            clients[len(clients) - 1].start()
            thread_cnt += 1
    elif(client_type == 'controller'):
        clients.append(Game_Client_Thread(thread_cnt, 'controller', addr, conn))
        clients[len(clients) - 1].start()
        thread_cnt += 1
    else:
        print("IDK what type of client yo ass trying to connect")


