#creds to Balaji as well for making the continous analysis function!

import socket, threading, json, contextlib, io, time
from random import *

synonyms = __import__("Project_3") #put your filename here (pls for the love of god run this shit in the same folder as your file (and for the love of jesus do not pyzo this))

HEADER = 16
DELAY = 0.0 #hehehehe
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
        received_message = self.client.recv(500000).decode(FORMAT)
        print(received_message)

    def send(self, function, data = ""):
        try:
            print(function +":" + str(data))
            self.client.send(str.encode(function +":" + str(data)))
            return self.client.recv(500000).decode(FORMAT)
        except socket.error as e:
            print(str(e))
            return False

    def get_sentences(self):
        return self.send("get_sentences")

    def get_dict(self):
         temp = self.send("get_dict")
         print("DICTIONARY: ", temp)
         return json.loads(temp)
        

class client():

    def __init__(self):
        self.network = Network()

    def run(self):
        not_ended = True
        print("Hello! Welcome to mrmandarin's synonyms testing program!")

        while(not_ended):
            print("Here are your options:")
            print("1 - Check Dict")
            #print("2 - Continuously Check Dict")
            print("3 - Exit")
            s = input()
            if(s == '3'):
                not_ended = False
            elif(s == '1'):
                self.check()
            elif(s == '2'):
                self.continuous_check()
            else:
                print("Dafuq you entered boii")

    def check(self):
        print('\n')
        #print("WE IN")
        sentences = self.network.get_sentences()
        mandarin_dict = self.network.get_dict()
        #print("SENTENCES:", sentences)
        #print(mandarin_dict)
        f = open("sample_case.txt", "w", encoding = "latin1")
        f.write(sentences)
        f.close()
        user_dict = synonyms.build_semantic_descriptors_from_files(["sample_case.txt"])
        #print('\n')
        print("COMPARING DICTIONARIES!")
        good = True
        for word in mandarin_dict.keys():
            if(not good):
                break
            values = mandarin_dict[word]
            for value in values.keys():
                try:
                    if(mandarin_dict[word][value] != user_dict[word][value]):
                        print("VALUES NOT MATCHING!")
                        print("WORD BEING INDEXED: ", word)
                        print("WORD NOT MATCHING: ", value)
                        print('\n')
                        print("Mandarin's Dict: ", values)
                        print("Your Dict: ", user_dict[word])
                        print('\n')
                        good = False
                        break
                except:
                    print("Something went wrong!")
                    print(f"An error occured when trying to index [{word}][{value}]")
                    print('\n')
                    good = False
                    break
        if(good):
            print("ALL GOOD!")
        else:
            print("Here's the sentences:")
            print(sentences)
            print("Here's Mrmandarin's dict:")
            print(mandarin_dict)
            print("Here's YOUR dict:")
            print(user_dict)
        return good

    def continuous_check(self):
        print("To exit, just quit the program. Fuck user usability.")
        cnt = 0
        while(True):
            if(self.check()):
                cnt += 1
                print("Number of test cases passed: ", cnt)
            else:
                break
        print(f"Well, you passed {cnt} cases...")


root = client()
root.run()
