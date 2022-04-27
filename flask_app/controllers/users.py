from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
import bcrypt
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    session['user_id'] = User.save(data)

    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {'email':request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid email/password. Try again", 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
        }
    this_user = User.get_all_by_id(data)
    all_sightings = Sighting.get_all()
    
    return render_template('dashboard.html', this_user = this_user, all_sightings = all_sightings)

