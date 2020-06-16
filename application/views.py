from flask import Flask, render_template, redirect, request, url_for, session, Blueprint, flash, jsonify
from flask_login import current_user
from application.database import Database, create_database_user

view = Blueprint('views', __name__, static_folder='static')
from main import socketio

USERKEY = 'user'

@view.route('/')
@view.route('/home')
def home():
  return render_template('home.html')


@view.route('/login', methods=['POST', 'GET'])
def login():

  if USERKEY in session:
      redirect(url_for('views.home'))
  db = Database()
  
  if request.method == 'POST':
    loginValues = request.form
    
    user = create_database_user(loginValues['emailInput'],loginValues['passwordinput'])
    isValid = db.validate_user(user)
    print(isValid)

    if isValid:
      session[USERKEY] = db.get_user_info(user)['name']
      return redirect(url_for('views.home'))
    else:
      flash('Invalid email/password')
  
  return render_template('login.html')

@view.route('/logout')
def logout():
  print('logged out client')
  try:
      session.pop(USERKEY, None)
  except:
      pass
  return redirect(url_for('views.home'))

@view.route('/register')
def register():
  return render_template('register.html')
