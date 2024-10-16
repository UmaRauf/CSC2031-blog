from app import db
from app import app
from datetime import datetime
from flask_login import UserMixin
import pyotp

class User(db.Model, UserMixin):
    __tablename__ = 'users'
   # __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    pin_key = db.Column(db.String(32), nullable=False, default=pyotp.random_base32())


    blogs = db.relationship('Post')

    def __init__(self, username, password, pin_key=None,role=None):
        self.username = username
        self.password = password
        if pin_key:
            self.pin_key = pin_key
        else:
            self.pin_key = pyotp.random_base32()


    def verify_password(self, password):
        return self.password == password

    def verify_pin(self, pin):
        return pyotp.TOTP(self.pin_key).verify(pin)


    def get_2fa_uri(self):
        return str(pyotp.totp.TOTP(self.pin_key).provisioning_uri(
            name=self.username,
            issuer_name='CSC2031 Blog'))

class Post(db.Model):
    __tablename__ = 'posts'
   # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey(User.username), nullable=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, username, title, body):
        self.username = username
        self.title = title
        self.body = body

    def update_post(self, title, body):
        self.title = title
        self.body = body
        db.session.commit()

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username='trollgito',password='nenekhg',role='user')
        db.session.add(user)
        db.session.commit()
        admin = User(username='username', password='password', role='admin')
        db.session.add(admin)
        db.session.commit()
