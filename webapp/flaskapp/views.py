import requests
import json

from flaskapp import app
from flaskapp.models import db, User, add_user_to_db
from flask import Flask, render_template, request
from .config import SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lights.db'
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False
app.secret_key = SECRET_KEY

# First time init, run python in webapp/
# >>> import flaskapp
# >>> flaskapp.models.db.create_all(app=flaskapp.app)

db.init_app(app)

@app.route('/')
def home():
    """
    List all users or add new user
    """
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/getmycolor', methods=['POST'])
def get_my_color():
    """
    called by particle when it wakes up
    """
    print("WOW")
    print(request.data)
    print(request.form)
    return "hello"


@app.route('/newuser', methods=['GET', 'POST'])
def add_user():
    """
    Create new user
    """
    if request.method == 'GET':
        users = User.query.all()
        return render_template('add.html', users=users)

    if request.method == 'POST':
        print(request.form['name'])
        add_user_to_db(db, request.form)
        return render_template('add.html')


@app.route('/user/<user_url>', methods=['GET', 'POST'])
def user_page(user_url):
    """
    User home page, can edit their settings from here
    Currently no authentication
    """
    current_user = User.query.filter(User.url == user_url).first()
    users = User.query.all().remove(current_user)

    if request.method == 'GET':
        return render_template('userpage.html', current_user=current_user, 
                                users=users, update=False)

    if request.method == 'POST':
        # TODO 
        # take POST data and update database
        sel_users = request.form.getlist('check')
        chosen_color = request.values['color']
        return render_template('userpage.html', current_user=current_user,
                                users=users, update=True)


@app.route('/touch/<user>')
def send_colors(user):
    """
    iterate over families
    find matching key
    send to all users in family
    """
    return render_template('base.html')


def update_chosen_colors(user, color):
    """
    change User's LED to Color
    """
    return render_template('base.html')

