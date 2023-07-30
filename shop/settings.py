from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_session import Session
from flask_login import LoginManager, current_user

from .import utils

app = Flask(
    __name__,
    instance_path=utils.BASE_DIR,
    template_folder=utils.BASE_DIR / "assets/templates",
    static_folder=utils.BASE_DIR / "assets/static"
)

# Secret Key
app.config["SECRET_KEY"] = utils.get_env_vars("SECRET_KEY", "top-secret")

# Flask_Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Vous devez vous connecter pour accéder à cette page."

# Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = utils.get_env_vars(
    "DATABASE_URL", f"sqlite:///{utils.BASE_DIR}/db.sqlite3"
)
db = SQLAlchemy(app)

# Urlconfig
from .import views
from .import auth

# Admin
from .import models
from .import admin as adm

admin = Admin(app, name="Admin", template_mode="bootstrap4")

admin.add_views(
    adm.ProductAdminView(models.Product, db.session)
)


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)

@app.before_request
def get_current_user():
    g.user = current_user