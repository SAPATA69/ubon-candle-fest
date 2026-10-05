from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ubcandle_db.sqlite"
# เชื่อมต่อ PostgreSQL บน Render โดยตรง
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubcf2026_vgrq_user:SfcyOvMHXXKjcbQ1MvDhWLLl48Hhbimz@dpg-daqafs8jo6nc73do59t0-a.virginia-postgres.render.com/ubcf2026_vgrq'

# ใช้ secret แบบพื้นฐานไปก่อน สำหรับการเรียนรู้ในขั้นแรก
app.config['SECRET_KEY'] = b'secretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import routes, models
