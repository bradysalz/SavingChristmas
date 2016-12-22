import requests
import json

from flask import Flask
from config import *


app = Flask(__name__)

@app.route('/')
def home():
    """
    pick janaki or karen
    """
    pass


@app.route('/<user>')
def pick_colors(user):
    """
    use same template for both families
    get/post it to update colors
    """
    pass


@app.route('/touch/<user>')
def send_colors(user):
    """
    iterate over families
    find matching key
    send to all users in family
    """
    pass


def update_chosen_colors(user, color):
    """
    change User's LED to Color
    """
    pass

