from flask import Blueprint, render_template,request, flash, redirect
from flask.helpers import url_for

from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# blueprint helps separte views
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            # check the password hash
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password!', category='error')
        else:
            flash('email does not exist', category='error')
    if current_user.is_authenticated:
        return redirect (url_for('views.home'))
    return render_template('login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name   = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('user already exist!', category='error')
        if len(email) < 4:
            flash('email must above 3 chracters', category='error')
        elif len(name) < 2:
            flash('name must be greater than a character', category='error')
        elif password != password2:
            flash('passwords must match', category='error')
        elif len(password) < 8:
            flash('password should be above 7 characters', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('account created', category='success')
            return redirect(url_for('auth.login'))
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return  redirect(url_for('auth.login'))