import socket
import pickle
import time



SERVER = '192.168.1.151'
PORT = 55555
ADDR=(SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)



client.send(bytes('paper',FORMAT))
input()
client.send(bytes('get',FORMAT))
input()
game = pickle.loads(client.recv(2048))

print(game.ready)

input()

