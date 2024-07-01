from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///guitarisland.db"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'