from datetime import datetime
import socket, sys, threading, json, time
from random import *
import synonyms

temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5555
SERVER = ''
FORMAT = 'utf-8'
HEADER = 2048
DELAY = 0.05

SERVER_IP = socket.gethostbyname(SERVER)

try:
    temp.bind((SERVER, PORT))

except socket.error as e:
    print(str(e))

temp.listen(2)
print("Waiting for a connection")


clients = []
f = open("words.txt", "r", encoding = "latin1")
words = f.read().split('\n')
f.close()

punctuation = [', ', '- ', '--', ': ', '; ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
separators = ['. ', '! ', '? ', '. ', '. ']

def get_punc():
    return punctuation[randint(0, len(punctuation) - 1)] 

def get_separator():
    return separators[randint(0, len(separators) - 1)]

def get_word():
    return words[randint(0, len(words) - 1)]

def randomize_cap(word):
    if(randint(0, 3)):
        return word.lower()
    return word.upper()

class Client_Thread(threading.Thread):

    def __init__(self, addr, conn, cnt):
        threading.Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        self.current_words = []
        self.num = cnt
        self.current_sentences = []

    def make_sentences(self):
        self.current_words = []
        self.current_words.clear()
        sentence = ""
        current_sentence = ""
        sentences = []
        for x in range(randint(2,6)):
            sz = len(sentence)
            y_range = randint(2, 5)
            words_in_sentence = []
            for y in range(y_range):
                word = words[randint(0, len(words) - 1)]
                if(word.lower() not in self.current_words):
                    self.current_words.append(word.lower())
                words_in_sentence.append(word)
                sentence += randomize_cap(word)
                sentence += get_punc()
            y1_range = randint(1, 2)
            for y in range(y1_range):
                sentence += randomize_cap(self.current_words[randint(0, len(self.current_words) - 1)])
                sentence += get_punc()
            y2_range = randint(1,2)
            for y in range(y2_range):
                sentence += randomize_cap(words_in_sentence[randint(0, len(words_in_sentence) - 1)])
                sentence += get_punc()
            sentence += get_separator() + '\n'
            words_in_sentence.clear()
            if(not randint(0, 2) and len(sentences)):
                sentence += sentences[randint(0,len(sentences) - 1)]
            sentences.append(sentence[sz:len(sentence)])
        #print("SENTENCES: ", sentences)
        self.current_sentences = sentence
        return sentence

    def get_my_output(self, sentence):
        f = open("sample_case" + str(self.num) + ".txt", 'w')
        f.write(sentence)
        f.close()
        self.current_dict = synonyms.build_semantic_descriptors_from_files(["sample_case" + str(self.num) + ".txt"])
        return self.current_dict

    def cosine_similarity(self, s):
        temp_dict = {}
        words = s.keys()
        for word in words:
            temp_dict[word] = {}
        for word1 in words:
            for word2 in words:
                if(word1 != word2):
                    temp_dict[word1][word2] = synonyms.cosine_similarity(s[word1], s[word2])
        return temp_dict


    def run(self):
        cnt = 0
        while True:
            if(cnt < 1000):
                try:
                    cnt += 1
                    data = self.conn.recv(2048).decode(FORMAT).split(':')
                    print(f"Received Data From {self.addr}")
                    print(data)
                    if(data[0] == 'get_sentences'):
                        cnt = 0
                        sentence = self.make_sentences()
                        self.conn.send(str.encode(self.make_sentences()))
                    elif(data[0] == 'get_dict'):
                        cnt = 0 
                        dict_ = json.dumps(self.get_my_output(self.current_sentences))
                        self.conn.send(str.encode(str(dict_)))
                    elif(data[0] == 'get_cos'):
                        cnt = 0
                        self.conn.send(str.encode(json.dumps(self.cosine_similarity(self.current_dict))))
                    time.sleep(DELAY)
                except Exception as e:
                    print("ERROR MESSAGE:", e)
                    print(f"Something with {self.addr} went wrong!")
                    self.conn.close()
                    break
            else:
                print("INFINITE LOOP!")
                self.conn.close()
                break
            cnt += 1

thread_cnt = 1
while True:
    try:
        conn, addr = temp.accept()
        print(conn, addr)
        print(f"Connection with {addr} established!")
        conn.send(str.encode("Connection with MrMandarin's Server established!"))
        clients.append(Client_Thread(addr, conn, thread_cnt))
        clients[len(clients) - 1].start()
        thread_cnt += 1
    except Exception as e:
        temp.close()
        print("ERROR MESSAGE: ", e)
        print("Error Connecting")

