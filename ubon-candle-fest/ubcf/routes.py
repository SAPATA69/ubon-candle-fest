from ubcf import db, app, bcrypt
from ubcf.models import User, Temple, Candle
import os, secrets
from datetime import date
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required
from flask import abort, render_template, redirect, jsonify, url_for, request, flash
from werkzeug.utils import secure_filename


def save_image(img):
  random_hex = secrets.token_hex(8)
  original_name = secure_filename(img.filename or '')
  if not original_name:
    return None
  _, fext = os.path.splitext(original_name)
  img_fn = random_hex + fext.lower()
  image_dir = os.path.join(app.root_path, 'static', 'images')
  os.makedirs(image_dir, exist_ok=True)
  img_path = os.path.join(image_dir, img_fn)

  img.save(img_path)

  return img_fn


def admin_required(view):
  from functools import wraps

  @wraps(view)
  @login_required
  def wrapped(*args, **kwargs):
    if current_user.role_id != 1:
      abort(403)
    return view(*args, **kwargs)

  return wrapped

@app.route('/')
def index():
  return render_template('index.html', title='Home Page')

@app.route('/user/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    user = db.session.scalar(db.select(User).where(
      (User.username == username) | (User.email == email)
    ))
    if user:
      flash('Username or email is already exists!', 'warning')
    elif not username or not email or not password:
      flash('Please fill in all fields.', 'warning')
      
    elif password != confirm_password:
      flash('Password is not match!', 'warning')
    else:
      password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
      new_user = User(username=username, email=email, password=password_hash)
      db.session.add(new_user)
      db.session.commit()
      flash('Register successfully. Please log in.', 'success')
      return redirect(url_for('login'))
      
  return render_template('/users/register.html', title='Register Page')

@app.route('/user/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    user = db.session.scalar(db.select(User).where(User.email==email))
    if user and bcrypt.check_password_hash(user.password, password):
      login_user(user)
      return redirect(url_for('index'))
    flash('Invalid email or password.', 'warning')
      
  return render_template('users/login.html', title='Login Page')

@app.route('/user/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/temples', methods=['GET', 'POST'])
@admin_required
def temples():
  temples = db.session.scalars(db.select(Temple)).all()
  return render_template('temples/temples.html', title='Show Temples', temples=temples)

@app.route('/temples/new_temple', methods=['GET', 'POST'])
@admin_required
def new_temple():
  if request.method == 'POST':
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    if not name:
      flash('Temple name is required.', 'warning')
      return render_template('temples/add_temple.html', title='New Temple')
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
    temple_id = request.form.get('temple_id', type=int)
    temple = db.session.get(Temple, temple_id)
    candle_name = request.files.get('candle_name')

    if temple is None:
      flash('Selected temple was not found.', 'warning')
      return redirect(url_for('new_candle'))
    if candle_name is None or not candle_name.filename:
      flash('Please select an image.', 'warning')
      return redirect(url_for('new_candle'))

    pic_file = save_image(candle_name)
    if pic_file is None:
      flash('Invalid image filename.', 'warning')
      return redirect(url_for('new_candle'))

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
