from flask import Flask
from app import create_app
from app.routes import routes

#app = create_app()

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'secret'
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
