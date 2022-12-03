from app import db, myapp_obj
from app.models import User, Post
from app.forms import LoginForm, RegisterForm, DeleteAccountForm, PostForm
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@myapp_obj.route('/')
@myapp_obj.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)

@myapp_obj.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/login')

@myapp_obj.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    db.session.delete(user)
    db.session.commit()
    return render_template('delete_account.html', title='Delete Account')

@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    current_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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

@myapp_obj.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='Create Post', form=form, legend='Create Post')

@myapp_obj.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('index'))

@myapp_obj.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
