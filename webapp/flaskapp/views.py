import requests
from flaskapp import app
from flaskapp.models import db, User, add_user_to_db
from flask import Flask, render_template, request, redirect, url_for
from .config import SECRET_KEY

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lights.db'
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
        return redirect(url_for('home'), code=302)


@app.route('/user/<user_url>', methods=['GET', 'POST'])
def user_page(user_url):
    """
    User home page, can edit their settings from here
    Currently no authentication
    """
    current_user = User.query.filter(User.url == user_url).first()
    users = User.query.all()
    users.remove(current_user)

    if users is None:
        users = []

    # TODO: @KAREN
    # Debug why this doesn't work
    # test.py checks all of this and passes
    # throws up an error about how it can't find the 
    # follower.id column in followers table
    is_following = [False if current_user.is_following(user) is None else True 
                    for user in users]
    followers = zip(users, is_following)

    if request.method == 'GET':
        return render_template('userpage.html', current_user=current_user, 
                                followers=followers, update=False)

    if request.method == 'POST':
        # TODO 
        # take POST data and update database
        sel_users = request.form.getlist('check')
        chosen_color = request.values['color']
        return render_template('userpage.html', current_user=current_user,
                                followers=followers, update=True)


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

