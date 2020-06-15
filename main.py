from flask import Flask, render_template, redirect, request, url_for, session
from flask_socketio import SocketIO
from flask_session import Session
from user import User
from game import Game
from application import create_app
from threading import Thread
import time

app = create_app()
socketio = SocketIO(app)

CLIENTGAMEKEY = 'clientGameKey'
USERKEY = 'user'

games = {}
idCount = 0

@socketio.on('start-game')
def handle_game(gameID):
    global idCount
    currentGame = games[gameID]

    while not currentGame.ready:
        time.sleep(2.5)
        print('searching for other player')
        print(session)
        if CLIENTGAMEKEY not in session:
            break
        

    while currentGame.ready:
        @socketio.on('move')
        def move(choice):
            print(choice)
        
        if CLIENTGAMEKEY not in session or currentGame.quit:
            break
    
    games.pop(gameID)
    idCount -= 1


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

        
    session[CLIENTGAMEKEY] = {'name':name,'gameID':gameID}
    print(gameID,session[CLIENTGAMEKEY]['gameID'])
    socketio.emit('client-game-setup',(gameID,session[CLIENTGAMEKEY]['gameID']))

    
    print(games)
    

@socketio.on('searching')
def searching():
    global idCount
    client_session = session.get(USERKEY,None)
    user = session.get(CLIENTGAMEKEY,None)


    if client_session == None: 
        return (url_for('views.login'))

    if not user:
        gameTracker(client_session)
    else:
        session.pop(CLIENTGAMEKEY,None)
    # else:
    #     if games[game.gameID].ready:
    #         print (user.get('gameID',None),game.gameID)
    #         socketio.emit('disconnect-client', (game.gameID, user.get('gameID',None)))
    #     else:
    #         idCount -=1
    #         session.pop(GAMEKEY,None)
    #     print(f'[DISCONNECT] {client_session} has lost connection')

@socketio.on('disconnect-other-client')
def disconnect_client(gameID):
    global idCount

    game = session.get(CLIENTGAMEKEY,None)
    print(f'[DISCONNECT] disconnecting {session[USERKEY]}')

    try:
        if game.gameID == gameID:
            idCount -= 1
            session.pop(CLIENTGAMEKEY,None)
            if game in games:
                games.pop(game)
    except:
        pass
        
@socketio.on('disconnect')
def disconnect():
    print(f'[CONNECTION ERROR] {session[USERKEY]} lost thread')
    try:
        session.pop(CLIENTGAMEKEY,None)
    except:
        pass

@socketio.on('stop-processes')
def stop_processes():
    print('called')
    print(session)
    if USERKEY in session:
        session.pop(CLIENTGAMEKEY,None)


if __name__ == '__main__':
    socketio.run(app,debug=True)

