import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv(".env")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


from guardioesverdade.routes import homepage