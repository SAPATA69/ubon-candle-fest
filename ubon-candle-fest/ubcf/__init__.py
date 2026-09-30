import os, secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# คอมเมนต์บรรทัด SQLite ออกเพื่อปิดการใช้งาน
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubcandle_db.sqlite'

# เปิดใช้งาน PostgreSQL โดยใส่เครื่องหมาย ' ' (Single quote) ครอบ Connection String
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubcf2026_vgrq_user:SfcyOvMHXXKjcbQ1MvDhWLLl48Hhbimz@dpg-daqafs8jo6nc73do59t0-a.virginia-postgres.render.com/ubcf2026_vgrq'

app.config['SECRET_KEY'] = b'secretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from . import routes, models