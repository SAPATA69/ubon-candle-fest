from ubcf import app

# import os, secrets
# from flask import Flask, jsonify, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ubcandledb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<username>:@<password>.mysql.pythonanywhere-services.com/<username>$<database_name>'
# db.init_app(app)

# class Temple(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100), nullable=False)
#   description = db.Column(db.Text, nullable=False)
#   images = db.relationship('Image', backref='temple', lazy=True)

#   def __repr__(self):
#     return '<Temple: {}>'.format(self.name)

# class Image(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   img_name = db.Column(db.String(100), nullable=False)

#   temple_id = db.Column(db.Integer, db.ForeignKey('temple.id'), nullable=False)
#   # temple = db.relationship('Temple', backref=db.backref('images', lazy=True))

#   def __repr__(self):
#     return '<Image: {}>'.format(self.img_name)

# def save_image(img):
#   random_hex = secrets.token_hex(8)
#   fn, fext = os.path.splitext(img.filename)
#   img_fn = random_hex + fext
#   img_path = os.path.join(app.root_path, 'static/images', img_fn)

#   img.save(img_path)

#   return img_fn

# @app.route('/')
# def index():
#   return render_template('index.html', title='Home Page')

# @app.route('/about')
# def about():
#   return render_template('about.html', title='About Page')

# @app.route('/temples', methods=['GET'])
# def temples():
#   temples = Temple.query.all()
#   return render_template('temples.html', title='Temples', temples=temples)

# @app.route('/temples/add', methods=['GET', 'POST'])
# def add_temple():
#   if request.method == 'POST':
#     name = request.form['name']
#     # print(name)
#     description = request.form['description']
#     temple = Temple(name=name, description=description)
#     db.session.add(temple)
#     db.session.commit()

#     return redirect(url_for('temples'))

#   return render_template('add_temple.html', title='New Temple')

# @app.route('/temples/detail/<int:id>', methods=['GET', 'POST'])
# def show_temple(id):
#   temple = Temple.query.get(id)
#   return render_template('show_temple.html', title='Show Temple Detail', temple=temple)

# @app.route('/images/add', methods=['GET', 'POST'])
# def add_image():
#   temples = Temple.query.all()
#   if request.method == 'POST':
#     temple_id = request.form['temple_id']
#     # temple = Temple.query.get(temple_id)
#     img_name = request.files['img_name']

#     if img_name:
#       pic_file = save_image(img_name)

#     image = Image(img_name=pic_file, temple_id=temple_id)
#     db.session.add(image)
#     db.session.commit()

#     return redirect(url_for('images'))


#   return render_template('add_image.html', title='New Image', temples=temples)

# @app.route('/images')
# def images():
#   images = Image.query.all()
#   return render_template('images.html', title='Images', images=images)

# @app.route('/uboncandlefest/api/temples', methods=['GET'])
# def temples_api():
#   data = Temple.query.all()
#   temples = []
#   for t in data:
#     temples.append({'id': t.id, 'name': t.name, 'description': t.description})

#   return jsonify(temples)

# @app.route('/uboncandlefest/api/temple_images/<int:id>', methods=['GET'])
# def images_api(id):
#   data = Image.query.filter(Image.temple_id==id).all()
#   images = []
#   for img in data:
#     images.append({'id': img.id, 'img_name': img.img_name, 'temple_name': img.temple.name})

#   return jsonify(images)

# if __name__ == '__main__':
#   with app.app_context():
#     db.create_all()
#   app.run(debug=True)