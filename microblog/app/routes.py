from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'Mike'},
            'body': 'GoT S8 sucks'
        },
        {
            'author': {'username': 'Kevin'},
            'body': 'Endgame is amazing!'
        }
    ]
    return render_template('index.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    # Handle for submit
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Invalid password.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # Log the user in.
        login_user(user, remember=form.remember_me.data)

        # Get next page if redirected here from login_required function
        next_page = request.args.get('next')

        # Check if next page exists and for security check if next_page is
        # a relative link. If not then redirect to the index (naughty hacker).
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
