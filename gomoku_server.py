from datetime import datetime
import socket, sys, threading, json
import gomoFUKu

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5555
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

clients = []

class Client_Thread(threading.Thread):

    def __init__(self, addr, conn):
        threading.Thread.__init__(self)
        self.addr = addr
        self.conn = conn

    def run(self):
        while True:
            try:
                data = self.conn.recv(2048).decode(FORMAT).split(':')
                if(data[0] == 'A'):
                    board = json.loads(data[1])
                    print("Requested Analysis for board: \n", gomoFUKu.print_board(board))
                    analysis = gomoFUKu.analysis(board)
                    print("Here's the analysis: \n", analysis)
                    self.conn.send(str.encode(analysis))
            except:
                print(f"AN ERROR HAS OCCURED WITH ADDR: {self.addr}!")
                break

while True:
    try:
        conn, addr = s.accept()
        print(f"Connection with {addr} established!")
        conn.send(str.encode("Connection with MrMandarin's Server established!"))
        clients.append(Client_Thread(addr, conn))
        clients[len(game_clients) - 1].start()
    except:
        print("FUCK CONNECTION ISSUE")

