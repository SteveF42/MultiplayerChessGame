from flask import Flask, render_template, redirect, request, url_for, session
from flask_socketio import SocketIO
from user import User
from game import Game
from application import create_app

app = create_app()
socketio = SocketIO(app)

games = {}
idCount = 0

def gameTracker(name):
    global idCount
    idCount += 1
    gameID = (idCount-1)//2

    playerNum = 0
    if idCount % 2 == 1:
        print('[GAME] new game created')
        games[gameID] = Game(gameID)
    else:
        print('[GAME] game started')
        playerNum = 1
        games[gameID].readyGame()
    
    session['game'] = User(name, playerNum, gameID)
    print(games)


@socketio.on('searching')
def searching():
    global idCount

    name = session.get('name',None)
    game = session.get('game',False)

    if name == None: 
        return (url_for('views.login'))

    if not game:
        gameTracker(name)
    else:
        if games[game.gameID].ready:
            socketio.emit('disconnect-client', game.gameID)
        else:
            idCount -=1
            session.pop('game',None)
        print(f'[DISCONNECT] {name} has disconnected')

@socketio.on('disconnect-other-client')
def disconnect_client(gameID):
    global idCount

    user = session.get('game',None)
    print(f'[DISCONNECT] disconnecting {session["name"]} printing session data {session}')

    if user.gameID == gameID:
        idCount -= 1
        session.pop('game',None)
        


if __name__ == '__main__':
    socketio.run(app,debug=True)
