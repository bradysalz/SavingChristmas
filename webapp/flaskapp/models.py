from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    SavingChristmas Light Node User
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # user name ("Brady")
    color = db.Column(db.String(6))  # hex color ("AB23E1")
    coreID = db.Column(db.String(64)) # particle photon ID
    following = db.Column(db.String(512)) # serialized list of followers, yolo
    url = db.Column(db.String(128))  # custom url (usually name + "home")
                                     # no leading / 

    def __init__(self, name, color, coreID, following, url=None):
        if url is None:
            url = (name + "home").lower()

        if url[0] == '/':
            url = url[1:]

        self.name = name
        self.color = color
        self.coreID = coreID
        self.following = following
        self.url = url



    def __repr__(self):
            return "<Christmas saved for {0}>".format(self.name)


def add_user(db, form):
    pass