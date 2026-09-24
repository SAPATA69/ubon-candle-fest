from ubcf import db, app, bcrypt
from ubcf.models import User, Temple, Candle
import os, secrets
from datetime import date
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, redirect, jsonify, url_for, request, flash


def save_image(img):
  random_hex = secrets.token_hex(8)
  fn, fext = os.path.splitext(img.filename)
  img_fn = random_hex + fext
  img_path = os.path.join(app.root_path, 'static/images', img_fn)

  img.save(img_path)

  return img_fn

@app.route('/')
def index():
  return render_template('index.html', title='Home Page')

@app.route('/user/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    user = db.session.scalar(db.select(User).where(User.username==username))
    if user:
      flash('Username is already exists!', 'warning')
      
    else:
      if password != confirm_password:
        flash('Password is not match!', 'warning')
      else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
      
  return render_template('/users/register.html', title='Register Page')

@app.route('/user/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = db.session.scalar(db.select(User).where(User.email==email))
    if user and bcrypt.check_password_hash(user.password, password):
      login_user(user)
      return redirect(url_for('index'))
      
  return render_template('users/login.html', title='Login Page')

@app.route('/user/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/temples', methods=['GET', 'POST'])
@login_required
def temples():
  temples = db.session.scalars(db.select(Temple)).all()
  return render_template('temples/temples.html', title='Show Temples', temples=temples)

@app.route('/temples/new_temple', methods=['GET', 'POST'])
@login_required
def new_temple():
  if request.method == 'POST':
    name = request.form['name']
    description = request.form['description']
    temple = Temple(name=name, description=description)
    db.session.add(temple)
    db.session.commit()
    flash('Add New Temple Successfully', 'success')
    return redirect(url_for('temples'))
  
  return render_template('temples/add_temple.html', title='New Temple')

@app.route('/candles/candles', methods=['GET', 'POST'])
@login_required
def candles():
  candles = db.session.scalars(db.select(Candle)).all()
  return render_template('candles/candles.html', title='Candles Page', candles=candles)

@app.route('/candles/new_candle', methods=['GET', 'POST'])
@login_required
def new_candle():
  temples = db.session.scalars(db.select(Temple)).all()
  if request.method == 'POST':
    temple_id = request.form['temple_id']
    temple = db.session.get(Temple, temple_id)
    candle_name = request.files['candle_name']

    if candle_name:
      pic_file = save_image(candle_name)

    candle = Candle(name=pic_file, temple=temple, user=current_user)
    db.session.add(candle)
    db.session.commit()

    flash('Add New Candle Successfully', 'success')
    return redirect(url_for('candles'))

  return render_template('candles/add_candle.html', title='New Candle', temples=temples)

@app.route('/api/uboncandlefest/users', methods=['GET'])
def users_api():
  data = db.session.scalars(db.select(User)).all()
  users = []
  for user in data:
    tmp_user = {'id': user.id, 'username': user.username, 'email': user.email}
    candles = []
    for candle in user.candles:
      tmp_candle = {'id': candle.id, 'name': candle.name, 'temple_name': candle.temple.name}
      candles.append(tmp_candle)
    tmp_user['candles'] = candles

    users.append(tmp_user)
  
  return jsonify(users)

@app.route('/api/uboncandlefest/temples', methods=['GET'])
def temples_api():
  data = db.session.scalars(db.select(Temple)).all()
  temples = []
  for t in data:
    temples.append({'id': t.id, 'name': t.name, 'description': t.description})
    
  return jsonify(temples)

@app.route('/api/uboncandlefest/candles', methods=['GET'])
def candles_api():
  data = db.session.scalars(db.select(Candle)).all()
  candles = []
  for candle in data:
    tmp_candle = {'id': candle.id, 'name': candle.name, 'temple_name': candle.temple.name, 'owner': candle.user.username}
    candles.append(tmp_candle)

  return jsonify(candles)

@app.route('/api/uboncandlefest/temples/<int:id>', methods=['GET'])
def get_temple_by_id(id):
  data = db.session.get(Temple, id)
  temple = {'id': data.id, 'name': data.name, 'description': data.description}
  candles = []
  for candle in data.candles:
    tmp_candle = {'id': candle.id, 'name': candle.name, 'owner': candle.user.username}
    candles.append(tmp_candle)
  temple['candles'] = candles

  return jsonify(temple)

@app.route('/api/uboncandlefest/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
  data = db.session.get(User, id)
  user = {'id': data.id, 'username': data.username, 'email': data.email}
  candles = []
  for candle in data.candles:
    tmp_candle = {'id': candle.id, 'name': candle.name, 'owner': candle.user.username}
    candles.append(tmp_candle)

  user['candles'] = candles

  return jsonify(user)

