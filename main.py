from flask import Flask, render_template, redirect, request, url_for, session
from flask_socketio import SocketIO
from flask_session import Session
from user import User
from game import Game
from application import create_app

app = create_app()
socketio = SocketIO(app)

GAMEKEY = 'game'
CLIENTGAMEKEY = 'clientGameKey'
USERKEY = 'user'

games = {}
idCount = 0

def gameTracker(name):
    global idCount
    idCount += 1
    gameID = (idCount-1)//2

    playerNum = 0
    if idCount % 2 == 1:
        print('[GAME] new game, searching for other connection')
        games[gameID] = Game(gameID)
    else:
        print('[GAME] connection found! Game starting')
        playerNum = 1
        games[gameID].readyGame()
    
    session[GAMEKEY] = User(name, playerNum, gameID)
    session[CLIENTGAMEKEY] = {'name':name,'gameID':gameID}
    print(games)
    


@socketio.on('searching')
def searching():
    global idCount
    client_session = session.get(USERKEY,None)
    user = session.get(CLIENTGAMEKEY,None)
    game = session.get(GAMEKEY,False)

    if client_session == None: 
        return (url_for('views.login'))

    if not game:
        gameTracker(user)
    else:
        if games[game.gameID].ready:
            print (user.get('gameID',None),game.gameID)
            socketio.emit('disconnect-client', (game.gameID, user.get('gameID',None)))
        else:
            idCount -=1
            session.pop(GAMEKEY,None)
        print(f'[DISCONNECT] {client_session} has disconnected')

@socketio.on('disconnect-other-client')
def disconnect_client(gameID):
    global idCount

    client = session.get(GAMEKEY,None)
    print(f'[DISCONNECT] disconnecting {session[USERKEY]} printing session data {session}')

    if client.gameID == gameID:
        idCount -= 1
        session.pop(GAMEKEY,None)
        session.pop(CLIENTGAMEKEY,None)




if __name__ == '__main__':
    socketio.run(app,debug=True)
