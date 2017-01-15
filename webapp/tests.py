# Thanks to Miguel Grinberg for this
# Heavily lifted from: 
# The Flask Mega-Tutorial Part VII: Unit Testing

import os
import unittest

from flaskapp import app
from flaskapp.models import User, db

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.app = app
        db.init_app(app)

        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        u = User(name="Brady")
        db.session.add(u)
        db.session.commit()
        qry = User.query.filter(User.name == "Brady").first()
        assert qry == u

    def test_remove_user(self):
        u = User(name="NoCopyJustRemove")
        db.session.add(u)
        db.session.commit()
        qry = User.query.filter(User.name == "NoCopyJustRemove").first()
        assert qry == u

        db.session.delete(qry)
        db.session.commit()
        qry = User.query.filter(User.name == "NoCopyJustRemove").first()
        assert qry is None

    def test_follow(self):
        u1 = User(name='john')
        u2 = User(name='susan')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().name == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().name == 'john'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

if __name__ == '__main__':
    unittest.main()