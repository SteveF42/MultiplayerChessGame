from flask import Flask, render_template, redirect, request, url_for, session, Blueprint, flash, jsonify
from flask_login import current_user
from application.database import Database, create_database_user

view = Blueprint('views', __name__, static_folder='static')
from main import socketio

USERKEY = 'user'

@view.route('/')
@view.route('/home')
def home():
  if USERKEY not in session:
    flash('Please log in','alert')
    return redirect(url_for('views.login'))
  return render_template('home.html')


@view.route('/login', methods=['POST', 'GET'])
def login():

  db = Database()
  current_user = session.get(USERKEY,None)
  
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
      return redirect(url_for('views.login',user=current_user))

  return render_template('login.html',user=current_user)

@view.route('/logout')
def logout():
  print('logged out client')
  try:
      session.pop(USERKEY, None)
  except:
      pass
  return redirect(url_for('views.login'))

@view.route('/register')
def register():
  return render_template('register.html')
