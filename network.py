import socket

class Network():
    def __init__(self,server):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = server
        self.port = 5555
        self.addr = (self.server,self.port)
        self.pos = self.connect()

    def get_Pos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode('utf-8')
        except:
            pass
    
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode('utf-8')
        except socket.error as e:
            print(e)
        
