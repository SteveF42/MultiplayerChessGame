from flask import Flask, render_template, redirect, request, url_for, jsonify,session, flash
from flask_socketio import SocketIO, join_room, leave_room
from user import User
from game import Game
from application import create_app
import time

app = create_app()
socketio = SocketIO(app,ping_timeout=20,ping_interval=10)

CLIENTGAMEKEY = 'clientGameKey'
USERKEY = 'user'

games = {}
user_games = {}
idCount = 0

#when game is in play these are used
@socketio.on('room-message')
def room_message(msg):
    room = session.get(CLIENTGAMEKEY)['gameID']
    data = {'message':msg,'name':session.get(USERKEY)}
    
    socketio.emit('received-message',data,room=room)


@socketio.on('play-game')
def game_choice(move):
    '''
    type move: str
    rtype: None
    '''
    gameID = session[CLIENTGAMEKEY]['gameID']
    playerNum = session[CLIENTGAMEKEY]['playerNum']
    game = games[gameID]

    game.set_player_move(playerNum-1,move)
    
    if game.both_players_went():
        winner = game.winner()
        
        socketio.emit('player-choice',(playerNum,winner,move),room=gameID)
        game.reset()
    else:
        socketio.emit('player-choice',(playerNum,None,move),room=gameID)


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

    join_room(gameID)
    
    if idCount % 2 == 1:
        session[CLIENTGAMEKEY] = {'name':name,'gameID':gameID,'playerNum':1}
        print('[GAME] new game, searching for other connection')

        game = Game(gameID)
        game.playerNames[0] = name;
        games[gameID] = game
        games[gameID].players[0] = request.sid


    else:
        print('[GAME] connection found! Game starting')

        session[CLIENTGAMEKEY] = {'name':name,'gameID':gameID,'playerNum':2}
        games[gameID].playerNames[1] = name
        games[gameID].readyGame()
        games[gameID].players[1] = request.sid  
        socketio.emit('client-game-setup',games[gameID].playerNames, room=gameID)
   
    #socketio.emit('client-game-setup',(session[CLIENTGAMEKEY]['gameID']))
    print(games)


@socketio.on('searching')
def searching():
    global idCount
    client_session = session.get(USERKEY,None)
    user = session.get(CLIENTGAMEKEY,None)

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

@socketio.on('get_player_num')
def get_user_id():
    if not session[USERKEY]:
        return

    playerNum = session[CLIENTGAMEKEY]['playerNum']
    return playerNum

if __name__ == '__main__':
    socketio.run(app,debug=True)
