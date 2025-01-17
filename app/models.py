from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Recepts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.String(128), nullable=False)
    recept = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Recepts {self.name}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))