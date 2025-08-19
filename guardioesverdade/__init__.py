import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message


from supabase import create_client

from dotenv import load_dotenv

load_dotenv(".env")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configurações do Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = (
    "login"  # Redireciona usuário para a tela de login caso não esteja logado
)
bcrypt = Bcrypt(app)
mail = Mail(app)


from guardioesverdade.routes import homepage, login
from guardioesverdade.api.mercadopago.mp_webhook import mercadopago_webhook
from guardioesverdade.api.mercadopago.mp_tasks import cron_verifica_assinaturas
from guardioesverdade.api.mercadopago.mp_api import gera_link_pagamento
from guardioesverdade.api.contato.flask_mail import enviar_email
from guardioesverdade.forms import UserForm, LoginForm
