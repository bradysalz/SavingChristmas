from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    """
    SavingChristmas Light Node User
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # user name ("Brady")
    color = db.Column(db.String(6))  # hex color ("AB23E1")
    coreID = db.Column(db.String(64)) # particle photon ID
    url = db.Column(db.String(128))  # custom url (usually name + "home")
                                     # no leading / 
    
    followed = db.relationship("User", 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref("followers", lazy="dynamic"),
                               lazy="dynamic")

    def __init__(self, name, color="", coreID="", url=None):
        if url is None:
            url = (name + "home").lower()

        if url[0] == "/":
            url = url[1:]

        self.name = name
        self.color = color
        self.coreID = coreID
        self.url = url

    def __repr__(self):
            return "<Christmas saved for {0}>".format(self.name)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


def add_user(db, form):
    pass