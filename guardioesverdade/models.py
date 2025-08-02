from flask_login import UserMixin

from guardioesverdade import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    plano = db.Column(db.String(50), nullable=False, default='gratuito')
    role = db.Column(db.String(20), nullable=False, default='user')
    data_criacao = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

