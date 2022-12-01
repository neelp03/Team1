from app import db, myapp_obj
from app.models import User, Post
from app.forms import LoginForm, RegisterForm, DeleteAccountForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@myapp_obj.route('/', methods=['GET', 'POST'])
@myapp_obj.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.all()
    if request.method == 'POST':
        logout_user(current_user)

    return render_template('index.html', title='Home', posts=posts)

@myapp_obj.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if form.password.data == current_user.password:
            db.session.delete(current_user)
            db.session.commit()
            flash('Your account has been deleted')
            return redirect(url_for('index'))
        else:
            flash('Incorrect password')
    return render_template('delete_account.html', title='Delete Account', form=form)

@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    current_form = LoginForm()

    if request.method == 'POST':
        user = User.query.filter_by(username=current_form.username.data).first()

        if user is None or not user.check_password(current_form.password.data):
            flash('Invalid Password!')
            return redirect('/login')

        login_user(user)
        return redirect('/')

    return render_template('login.html', title='Sign In', form=current_form)

@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    current_form = RegisterForm()

    if request.method == 'POST':
        user = User.query.filter_by(username=current_form.username.data).first()

        if user is not None:
            flash('This user exists already!')
            return redirect('/register')
        elif current_form.password.data != current_form.confirmPassword.data:
            flash ('Passwords do not match!')
            return redirect('/register')

        newUser = User(username=current_form.username.data, email=current_form.email.data, password_hash=current_form.password.data)
        newUser.set_password(newUser.password_hash)
        db.session.add(newUser)
        db.session.commit()
        flash('Account Created! Please login.')
        return redirect('/login')

    return render_template('register.html', title='Register', form=current_form)

