from webapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""
    __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=False, nullable=True)
    email = db.Column(db.String(40), index=True, unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    # website = db.Column(db.String(60), index=False, unique=False, nullable=True)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# class User(db.Model):
#     """Model for user accounts."""
#     __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), index=False, unique=True, nullable=True)
    # email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    # password = db.Column(db.String(80), index=False, unique=False, nullable=False)
    # bio = db.Column(db.Text, index=False, unique=False, nullable=True)
    # created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    # active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    # active_since = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    # admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)
