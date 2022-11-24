from app import db, myapp_obj
from app.models import User, Post
from app.forms import DeleteAccountForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@myapp_obj.route('/')
@myapp_obj.route('/index')
@login_required
def index():
    posts = Post.query.all()
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
    return render_template('login.html', title='Sign In')

@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register')

