from datetime import datetime
import socket, sys, threading
import network_ai

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5055
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
                data = json.loads(self.conn.recv(2048).decode(FORMAT))
                print(data)
                sending = network_ai.pong_ai((data[0], data[1]), (data[2], data[3]), (data[4], data[5]))
                print("SENDING: ", sending)
                conn.send(str.encode(sending))
            except Exception as e:
                print("ERROR: ", e)
                print("AN ERROR HAS OCCURED!")
                self.conn.close()
                break

thread_cnt = 0

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

