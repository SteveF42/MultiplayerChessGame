import socket
import threading
import pickle
import math
from flask import jsonify
from game import Game


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 55555
ADDR=(SERVER,PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

idCount = 0
games = {}


def handle_client(conn,p,gameID):
    '''
    type conn: User Connection
    type p: int range(0,1)
    type gameID: int
    '''
    global idCount
    global games
    print(f'playeID = {p}, connected to gameID {gameID}')

    
    while True:
        try:
            data = conn.recv(2048).decode(FORMAT)
            print(data)
            if gameID in games:
                game = games[gameID]

                if not data: 
                    break;
                elif data =='{quit}':
                    break
                elif data != "get":
                    game.set_player_move(p,data)
                else:
                    reply = game
                    conn.send(pickle.dumps(reply))
            else:
                break
            
        except Exception as e:
            print('[EXCEPTION]',e)
            break

    print(f'[DISCONNECT] client has disconnected from game {gameID}')
    idCount -= 1
    
    try:
        del games[gameID]
    except:
        pass

    conn.close()


def start():
    global games
    global idCount
    print(f'[LISTENING] server started listening on {SERVER}')
    server.listen()

    while True:

        try:
            conn, addr = server.accept()
            print(f'[CONNECTION] new connection at {addr}')
            idCount += 1

            gameID = (idCount-1)//2
            playerID = 0
            if idCount % 2 == 1:
                games[gameID] = Game(gameID)
                print('creating a new game')
            else:
                games[gameID].readyGame()
                playerID = 1

            thread = threading.Thread(target=handle_client,args=(conn,playerID,gameID))
            thread.start()


        except Exception as e:
            print('[EXCEPTION]',e)
    


if __name__ == '__main__':
    print('[START] server has started')
    start()