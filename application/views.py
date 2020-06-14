from flask import Flask, render_template, redirect, request, url_for, session, Blueprint, flash, jsonify
from application.database import Database, create_database_user

view = Blueprint('views', __name__, static_folder='static')


@view.route('/')
@view.route('/home')
def home():
    return render_template('home.html')


@view.route('/login', methods=['POST', 'GET'])
def login():

  if 'name' in session:
      redirect(url_for('/'))
  db = Database()
  
  if request.method == 'POST':
    loginValues = request.form
    print(loginValues)

    user = create_database_user(loginValues['emailInput'],loginValues['passwordinput'])

    isValid = db.validate_user(user)
    print(isValid)

    if isValid:
      print('valid user')
      return redirect(url_for('views.home'))
    else:
      flash('Invalid email/password')
  
  return render_template('login.html')

@view.route('/logout')
def logout():
  print('logged out client')
  try:
      session.pop('name', None)
      session.pop('game', None)
  except:
      pass
  return redirect(url_for('views.home'))

@view.route('/register')
def register():
  return render_template('register.html')

@view.route('/getGameId')
def getGameId():
  myGameId = session.get('game',None)

  if myGameId != None:
    return myGameId.gameID
  else:
    return None
