import requests
import json

from flaskapp import app
from flaskapp.models import db, User, add_user
from flask import Flask, render_template, request
from .config import SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lights.db'
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False
app.secret_key = SECRET_KEY

# First time init, run python in flaskapp/
# >>> import flaskapp
# >>> flaskapp.models.db.create_all(app=flaskapp.app)

db.init_app(app)

@app.route('/')
def home():
    """
    pick janaki or karen
    """
    with open('flaskapp/users.json', 'r') as f:
        users = json.load(f)

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
    if request.method == 'GET':
        return render_template('add.html')

    if request.method == 'POST':
        print(request.form)
        return render_template('add.html')

@app.route('/user/<username>', methods=['GET', 'POST'])
def pick_colors(username):
    with open('flaskapp/users.json', 'r') as f:
        users = json.load(f)

    users = [users[user] for user in users if users[user]['url'] != username]
    
    if request.method == 'GET':
        return render_template('userpage.html', users=users, update=False)

    if request.method == 'POST':
        sel_users = request.form.getlist('check')
        chosen_color = request.values['color']
        return render_template('userpage.html', users=users, update=True)

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

