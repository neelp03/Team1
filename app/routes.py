from app import db, myapp_obj
from app.models import User, Post, Message
from app.forms import LoginForm, RegisterForm, MessageForm, PostForm
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

@myapp_obj.route('/like/<int:post_id>', methods=['GET', 'POST'])
def like(post_id):
    post = Post.query.get_or_404(post_id)
    post.incLikes()
    flash('You liked the post!')
    db.session.commit()
    return redirect(url_for('index'))

@myapp_obj.route('/dislike/<int:post_id>', methods=['GET', 'POST'])
def dislike(post_id):
    post = Post.query.get_or_404(post_id)
    post.incDislikes()
    flash('You disliked the post!')
    db.session.commit()
    return redirect(url_for('index'))

@myapp_obj.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/login')

@myapp_obj.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        posts = Post.query.filter_by(author=current_user)
        for post in posts:
            db.session.delete(post)
            db.session.commit()
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        db.session.commit()
        return redirect('/login')
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

@myapp_obj.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('index'))

@myapp_obj.route('/user_profile', methods=['GET'])
def user_profile():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    print (current_user.followed)

    if user is None:
        flash("User does not exist")
        return redirect('/index')
    return render_template('user_profile.html', title='User profile', user=user, current_user=current_user)

@myapp_obj.route('/follow/<string:username>',  methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect('/user_profile?username='+username)
    current_user.follow(user)
    print (current_user.followed)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect('/user_profile?username='+username)

# unfollow user
@myapp_obj.route('/unfollow/<username>',  methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect('/user_profile?username='+username)


@myapp_obj.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@myapp_obj.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user_profile', username=recipient))
    return render_template('send_message.html', title='Send Message', form=form, recipient=recipient)

@myapp_obj.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    messages = current_user.received_messages.order_by(Message.timestamp.desc())
    return render_template('messages.html', messages=messages)
