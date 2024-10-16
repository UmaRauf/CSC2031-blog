import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_qrcode import QRcode

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO') == 'True'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

db = SQLAlchemy(app)
qrcode = QRcode(app)

from main.views import main_blueprint

app.register_blueprint(main_blueprint)

from blog.views import blog_blueprint

app.register_blueprint(blog_blueprint)

from users.views import users_blueprint

app.register_blueprint(users_blueprint)

from admin.views import admin_blueprint

app.register_blueprint(admin_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run()
