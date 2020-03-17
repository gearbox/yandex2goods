from webapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import class_mapper, ColumnProperty
from flask_sqlalchemy import inspect


class User(UserMixin, db.Model):
    """Model for user accounts."""
    __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=False, nullable=True)
    email = db.Column(db.String(40), index=True, unique=True, nullable=False)
    password = db.Column(db.String(200), index=False, unique=False, nullable=False)
    #
    company_name = db.Column(db.String(100), index=False, unique=False, nullable=True)
    shop_name = db.Column(db.String(100), index=False, unique=False, nullable=True)
    shop_url = db.Column(db.String(60), index=False, unique=False, nullable=True)
    # shop_currency = db.Column(db.String(3), index=False, unique=False, nullable=True)
    shop_currency = db.relationship('Currency', backref='flasklogin-users', lazy=True)
    # shop_outlet = db.Column(db.String(64), index=False, unique=False, nullable=True)
    shop_outlet = db.relationship('Outlet', backref='flasklogin-users', lazy=True)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    # bio = db.Column(db.Text, index=False, unique=False, nullable=True)
    # active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    # active_since = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    # admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        # return [prop.key for prop in class_mapper(self.__class__).iterate_properties
        #         if isinstance(prop, ColumnProperty)]
        # return [prop.key for prop in inspect(self.__class__).iterate_properties
        #         if isinstance(prop, ColumnProperty)]
        return [prop.key for prop in inspect(self.__class__).iterate_properties]

    def __repr__(self):
        return f'<User {self.username}>'


class Currency(db.Model):
    """Currencies"""
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), nullable=False)

    def __repr__(self):
        return f'<Currency {self.name}>'


class Outlet(db.Model):
    """Outlets"""
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    outlet = db.Column(db.Integer, nullable=False)
    instock = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), nullable=False)

    def __repr__(self):
        return f'<Outlet id: {self.outlet}, stock: {self.instock}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Category name: {self.name}, id: {self.index}>'
