from app import db
from datetime import datetime
from flask.ext.scrypt import generate_password_hash, generate_random_salt, check_password_hash, enbase64, debase64


#test data
class Test(db.Model):

    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    test_string = db.Column(db.Text(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# the user class
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(200), default='http://www.comicbookmovie.com/images/uploads/nerd.jpg')
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    salt = db.Column(db.String(120))
    posts = db.relationship('Test', backref='author', lazy='dynamic')


    # create the user 
    def __init__(self, password):
        self.timestamp = datetime.utcnow()

        # add some salt then cook up the hash
        self.salt = generate_random_salt()
        self.password_hash = generate_password_hash(password, self.salt)


    # flask-login default functions
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.email)

