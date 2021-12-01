from enum import unique
from flask import Flask, render_template, redirect, url_for
#form input
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#Database import
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
 
app = Flask("__name__", template_folder='affairs/Templates', static_folder='affairs/static')
app.config['SECRET_KEY'] = "affairs"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kelurahan.db'

ckeditor = CKEditor(app)
app.config['CKEDITOR_HEIGHT'] = 400
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from affairs.admin.routes import admingam
app.register_blueprint(admingam)








