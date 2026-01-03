from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app