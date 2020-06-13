from flask import Flask, render_template, redirect, request, url_for, session

def create_app():
    app = Flask(__name__)

    with app.app_context():
        
        from application.views import view  
        app.register_blueprint(view, url_prefix='/')
        app.secret_key = 'fhdjsalhfdslauihufinbv8w9'
        
        return app 
