from flask import Flask, render_template, redirect, request, url_for, session, Blueprint, flash, jsonify
from flask_login import current_user
from application.database import Database, create_database_user
import re

view = Blueprint('views', __name__, static_folder='static')
from main import socketio

USERKEY = 'user'


def validateCharacters(info):
  '''
  type info: dict
  rtype bool
  '''
  whiteSpace = re.compile(r'\s')
  special_character= re.compile(r'[!#$%^&*\(\)\{\}\[\]\:\;\'\"\<\>\,\?\/]')
  userInfo = info.values()
  for data in userInfo:
    if whiteSpace.search(data):
      flash('Invalid Input','info')
      return False
    if special_character.search(data):
      flash('Invalid Input','info')
      return False    
      
  return True

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

    user = create_database_user(loginValues['emailInput'],loginValues['passwordInput'])
    isValid = db.validate_user(user)

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

@view.route('/register',methods=['POST','GET'])
def register():
  db = Database()
  print(db.get_all_users())
  if request.method=='POST':
    
    form = request.form
    email1 = form['email']
    email2 = form['email2']
    if email1 != email2:
      flash('Emails do not match','info')
      return redirect(url_for('views.register'))
    
    user = create_database_user(form['email'],form['password'],form['username'])
    
    if validateCharacters(user):
      if db.check_existing_users(user['name'],user['email']):
        flash('Invalid Username/Email','info')
        return redirect(url_for('views.register')) 
      else:
        db.insert_new_user(user)
        session[USERKEY] = user['name']
        return redirect(url_for('views.home'))

    else:
      return redirect(url_for('views.register'))

  return render_template('register.html')

