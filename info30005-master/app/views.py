from flask import render_template, flash, redirect, session, url_for, request, abort, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegistrationForm, TestDataForm, ButtonForm
from .models import User, Test


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home', user=current_user)


@app.route('/')
@app.route('/test', methods=('GET', 'POST'))
@login_required
def test():

    form = TestDataForm()

    if form.validate_on_submit():
        test_entry = Test(test_string = request.form['test_string'], user_id = current_user.id)
        db.session.add(test_entry)
        db.session.commit()
        
    test = Test.query.all()

    return render_template('test.html', title='Test', form=form, user=current_user, data=test)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Test.query.get(id)
    if post is None:
        return redirect(url_for('test'))
    if post.author.id != current_user.id:
        return redirect(url_for('test'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('test'))

@app.route('/register', methods=('GET', 'POST'))
def register():

    # send user to index if logged in
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.password.data)
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # send user to index if logged in
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    
    # create the login form
    form = LoginForm()
    
    # log the user in if they are valid
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/topsecret')
@login_required
def topsecret():
    return render_template('topsecret.html', title='Top Secret', user=current_user)


