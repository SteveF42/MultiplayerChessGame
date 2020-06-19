from flask import Flask, render_template, redirect, request, url_for, jsonify,session, flash
from flask_socketio import SocketIO, join_room, leave_room
from user import User
from game import Game
from application import create_app
import time

app = create_app()
socketio = SocketIO(app,ping_timeout=10,ping_interval=5)

CLIENTGAMEKEY = 'clientGameKey'
USERKEY = 'user'

games = {}
user_games = {}
idCount = 0

@socketio.on('room-message')
def room_message(msg):
    print(msg)
    room = session.get(CLIENTGAMEKEY)['gameID']
    data = {'message':msg,'name':session.get(USERKEY)}
    
    socketio.emit('received-message',data,room=room)

@socketio.on('game-info')
def handle_game(msg):
    print(msg)
    return "Received"

def gameTracker(name):
    '''
    type name: str
    '''
    global idCount
    idCount += 1
    gameID = (idCount-1)//2

    session[CLIENTGAMEKEY] = {'name':name,'gameID':gameID,'sid':request.sid}
    join_room(gameID)
    
    if idCount % 2 == 1:
        print('[GAME] new game, searching for other connection')
        games[gameID] = Game(gameID)
        games[gameID].players[0] = request.sid

    else:
        print('[GAME] connection found! Game starting')
        games[gameID].readyGame()
        games[gameID].players[1] = request.sid  
        socketio.emit('client-game-setup',(session[CLIENTGAMEKEY]), room=gameID)
   
    #socketio.emit('client-game-setup',(session[CLIENTGAMEKEY]['gameID']))
    
    print(games)
    

@socketio.on('searching')
def searching():
    global idCount
    client_session = session.get(USERKEY,None)
    user = session.get(CLIENTGAMEKEY,None)
    print(client_session,request.sid)

    if client_session == None: 
        return url_for('views.login')
    
    if not user:
        gameTracker(client_session)
        return (None,True)
    else:
        idCount -= 1
        leave_room(session[CLIENTGAMEKEY]['gameID'])
        session.pop(CLIENTGAMEKEY,None)
        return (None,False)
    
         

@socketio.on('disconnect')
def disconnect():
    try:
        print(f'[CONNECTION ERROR] {session[USERKEY]} lost thread')
        info = session.get(CLIENTGAMEKEY,None)

        if info:
            gameID = info['gameID']
            if gameID in games:
                games.pop(gameID)
                socketio.emit('force-end-game',session[USERKEY],room=gameID)                
        session.pop(CLIENTGAMEKEY,None)
    except:
        pass

@socketio.on('pop-gamekey')
def stop_processes():
    if USERKEY in session:
        try:
            session.pop(CLIENTGAMEKEY,None)
        except:
            pass

@socketio.on('get-client-id',namespace='/private')
def get_user_id():
    id = session.get(CLIENTGAMEKEY)
    return request.sid



if __name__ == '__main__':
    socketio.run(app,debug=True)

