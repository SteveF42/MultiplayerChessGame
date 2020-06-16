import socket
import pickle

class Client:
    SERVER = '192.168.1.151'
    PORT = 55555
    ADDR=(SERVER,PORT)
    FORMAT = 'utf-8'
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __init__(self, name):
        self.client.connect(self.ADDR)
        self.name = name
        self.hasMoved = False
        self.game = None
    
    def disconnect(self):
        try:
            self.client.send(bytes('{quit}',self.FORMAT))
        except:
            pass

    def receiveGame(self):
        self.client.send('get')
        self.game = pickle.loads(self.conn.recv(2048))
        return self.game
    
    def sendMove(self,move):
        self.conn.send(move)
    
        