from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        
        from application.views import view  
        from application.database import Database, create_database_user
        app.register_blueprint(view, url_prefix='/')
        app.secret_key = 'fhdjsalhfdslauihufinbv8w9'
        
        return app 
