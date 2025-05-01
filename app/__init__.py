from flask import Flask
from .routes import routes

def create_app():
    app = Flask(__name__, template_folder='app/templates')
    
    from app.routes import main
    app.register_blueprint(main)

    return app
