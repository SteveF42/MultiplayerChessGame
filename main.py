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
@socketio.on('game-start')
def handle_game(gameID):
    global idCount
    game = games[gameID]
    user = session[USERKEY]
    if CLIENTGAMEKEY not in session:
        return

    while not game.ready:
        if CLIENTGAMEKEY not in session:
            break
        time.sleep(2.5)
        print(f'{user} searching for other player')

    
    gameover = False
    while games[gameID].ready and CLIENTGAMEKEY in session:
        time.sleep(1)
        @socketio.on('move')
        def move(choice):
            print(choice)
            if choice == 'DONE':
                gameover = True
        if gameover:
            print('[GAMEOVER] SOMEONE LOST')
            break;
        
        if CLIENTGAMEKEY not in session or games[gameID].quit:
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
    socketio.emit('client-game-setup',(session[CLIENTGAMEKEY]['gameID']),brodcast=False)
    
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
    
         

@socketio.on('server-disconnect')
def disconnect():
    try:
        print(f'[CONNECTION ERROR] {session[USERKEY]} lost thread')
        session.pop(CLIENTGAMEKEY,None)
    except:
        pass

@socketio.on('stop-processes')
def stop_processes():
    if USERKEY in session:
        try:
            session.pop(CLIENTGAMEKEY,None)
        except:
            pass

@socketio.on('get-client-id')
def get_user_id():
    id = session.get(CLIENTGAMEKEY)
    socketio.emit('response',id)
    

if __name__ == '__main__':
    socketio.run(app,debug=True)

