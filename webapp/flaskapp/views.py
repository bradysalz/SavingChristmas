import requests
import json

from flaskapp import app
from flask import Flask, render_template
from .config import *


@app.route('/')
def home():
    """
    pick janaki or karen
    """
    with open('flaskapp/users.json', 'r') as f:
        users = json.load(f)

    return render_template('home.html', users=users)


@app.route('/<username>')
def pick_colors(username):
    """
    use same template for both families
    get/post it to update colors
    """

    with open('flaskapp/users.json', 'r') as f:
        users = json.load(f)

    users = [users[user] for user in users if users[user]['url'] != username]
    return render_template('userpage.html', users=users)


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

