from flask import Flask
from app import create_app
from app.routes import routes
from werkzeug.middleware.proxy_fix import ProxyFix

#app = create_app()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = '7afiI8theB0SSfor3v3r'

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.register_blueprint(routes)

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000, debug=False)
