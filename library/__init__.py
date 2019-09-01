from flask import Flask
from flask_bootstrap import Bootstrap
from flask import request, redirect, render_template, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from library.helpers import _allowed_image, _allowed_image_filesize, _get_sort, get_bucket, get_s3_url
from library.forms import LoginForm
from library.user import User
from werkzeug.utils import secure_filename
from hurry.filesize import size
from hurry.filesize import alternative

import os
import datetime

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@app.route('/', methods=['GET', 'POST'])
def home():
	sort = _get_sort(app,'newest-to-older')
	
	if request.method == 'POST':
		if request.form.getlist('id'):
			sort = _get_sort(app,request.form.get('id'))

	photos = app.config['PHOTOS_COLLECTION'].find({"approved": True},{"url": 1,"likes":1}).sort(sort["field"], sort['order'])
	return render_template('home.html', sort=sort['description'] ,photos=list(photos))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		
		user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
		if user and User.validate_login(user['password'],form.password.data):
			# user_obj = User(user['_id'], user['couple'])
			user_obj = User(user)
			login_user(user_obj)
			flash("Logged in successfully!", category='success')

			return redirect(request.args.get("next") or url_for("home"))

		flash("Wrong username or password!", category='error')

	return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@lm.user_loader
def load_user(username):
	u = app.config['USERS_COLLECTION'].find_one({"_id": username})
	if not u:
		return None
	return User(u)

@app.route('/send')
def send():
	my_bucket = get_bucket(app)
	summaries = my_bucket.objects.all()
	return render_template('files.html', my_bucket=my_bucket, files=summaries)	

@app.route('/approve', methods=['GET', 'POST'])
@login_required
def approve():
	photos = app.config['PHOTOS_COLLECTION'].find({"approved": False},{"url": 1}).sort("date", -1)
	return render_template('approve.html', photos=list(photos))

@app.route('/upload', methods=['POST'])
def upload():
	if request.files:
		if "filesize" in request.cookies:

				if not _allowed_image_filesize(app,request.cookies["filesize"]):
					# print("Filesize exceeded maximum limit")
					flash("Filesize exceeded maximum limit of " + size(app.config["MAX_IMAGE_FILESIZE"])
						 + size(int(request.cookies["filesize"])), category='error')
					return redirect(request.url)

				print(request.files)
				image = request.files["image"]

				if image.filename == "":
					print("No filename")
					return redirect(request.url)

				if _allowed_image(app, image.filename):
					filename = secure_filename(image.filename)

					my_bucket = get_bucket(app)
					my_bucket.Object(image.filename).put(Body=image, ACL='public-read')

					url = get_s3_url(app, str(image.filename))

					photo = {
						"_id":image.filename,
						"url":url,
						"approved":False,
						"likes":0,
						"date":datetime.datetime.now()
						}

					app.config['PHOTOS_COLLECTION'].insert(photo)

					flash("Image "+image.filename+" send!", category='success')

					return redirect(url_for('send'))

				else:
					flash("File extensions allowed: jpeg, jpg, png, gif", category='error')
					return redirect(url_for('send'))

	else:
		flash("No file chosen", category='error')
	return redirect(url_for('send'))

@app.route('/approved', methods=['GET', 'POST'])
def approved():
	if request.method == 'POST':
		if request.form.getlist('id'):
			image_id = request.form.get('id')
			app.config['PHOTOS_COLLECTION'].update_one({"_id":image_id},{ "$set": {"approved":True}})
	
	return redirect(url_for('approve'))

@app.route('/like', methods=['GET', 'POST'])
def like():
	if request.method == 'POST':
		if request.form.getlist('id'):
			image_id = request.form.get('id')
			likes = app.config['PHOTOS_COLLECTION'].find_one({"_id": image_id},{"_id":0,"likes":1})['likes']+1
			app.config['PHOTOS_COLLECTION'].update_one({"_id":image_id},{ "$set": {"likes":likes}})
	
	return redirect(url_for('home'))