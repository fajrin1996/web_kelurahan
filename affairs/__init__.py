from enum import unique
from flask import Flask, render_template, redirect, url_for
#form input
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from affairs.admin.routes import admingam

#Database import
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
 
app = Flask("__name__", template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "affairs"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kelurahan.db'
app.register_blueprint(admingam)

ckeditor = CKEditor(app)
app.config['CKEDITOR_HEIGHT'] = 400
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)










