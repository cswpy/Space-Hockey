import socket
from _thread import *
import sys

server = '10.225.66.246'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print('Server loading...')

def thread_client(conn):
    conn.send(str.encode('Connected'))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            string = 'I am Phillip'
            if not data:
                print('Disconnected')
                break
            else:
                print('Received: ',reply)
                print('Sending: ',string)

            conn.sendall(str.encode(string))
        
        except:
            break
    
    print('Connection lost.')
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ",addr)
    start_new_thread(thread_client,(conn,))
