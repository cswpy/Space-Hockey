import socket
from _thread import *
import sys

port = 5555

class Server():
    def __init__(self):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.hostname)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.bind((server,port))
        except socket.error as e:
            print(str(e))
        
        self.server.listen(1)
        print('Server loading...')

        conn, addr = self.server.accept()
        print("Connected to: ",addr)
        start_new_thread(self.thread_client,(conn))

    def thread_client(conn):
        conn.send(str.encode('Connected to:'+str(self.host_name)+'@'+str(self.host_ip)))
        reply = ''
        while True:
            try:
                data = conn.recv(2048).decode('utf-8')
                
                if not data:
                    print('Disconnected')
                    break
                else:
                    print('Received: ',data)
                    print('Sending: ',string)

                conn.sendall(str.encode(string))
            
            except:
                break
        
        print('Connection lost.')
        conn.close()
