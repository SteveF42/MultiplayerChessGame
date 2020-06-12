from flask import Flask, render_template, redirect, request, url_for, session, Blueprint

view = Blueprint('views',__name__,static_folder='static')


@view.route('/')
@view.route('/home')
def home():
    return render_template('home.html')

@view.route('/login', methods=['POST','GET'])
def login():

    if 'name' in session:
        redirect(url_for('/'))

    if request.method == 'POST':
        name = request.form['username']
        print(name)

        if len(name) < 1:
            return redirect(url_for('views.login'))
        else:
            session['name'] = name
            
        return redirect(url_for('views.home'))
    else:
        return render_template('login.html')


@view.route('/logout')
def logout():
    print('logged out client')
    try:
        session.pop('name',None)
        session.pop('game',None)
    except:
        pass
    return redirect(url_for('views.home'))