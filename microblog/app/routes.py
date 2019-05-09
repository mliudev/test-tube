from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
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


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
