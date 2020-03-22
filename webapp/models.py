from flask_login import UserMixin
# from sqlalchemy.orm import class_mapper, ColumnProperty
from flask_sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db


class User(UserMixin, db.Model):
    """Model for user accounts."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), index=True, unique=True, nullable=False)
    #
    shop_name = db.Column(db.String(100), index=False, unique=False, nullable=True)
    company_name = db.Column(db.String(100), index=False, unique=False, nullable=True)
    shop_url = db.Column(db.String(60), index=False, unique=False, nullable=True)
    shop_currencies = db.relationship('Currency', backref='users', lazy=True, uselist=False)
    shop_outlets = db.relationship('Outlet', backref='users', lazy=True)
    product_categories = db.relationship('Category', backref='users', lazy=True)
    #
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    #
    password = db.Column(db.String(200), index=False, unique=False, nullable=False)
    # bio = db.Column(db.Text, index=False, unique=False, nullable=True)
    # active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    # active_since = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    # admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.email

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        # return [prop.key for prop in inspect(self.__class__).iterate_properties
        #         if isinstance(prop, ColumnProperty)]
        return [prop.key for prop in inspect(self.__class__).iterate_properties]

    def __repr__(self):
        return f'<User {self.email}>'


class Currency(db.Model):
    """Currencies"""
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False, default=1)
    auto_rate = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Currency {self.name}>'


class Outlet(db.Model):
    """Outlets"""
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    outlet_id = db.Column(db.Integer, nullable=False)
    instock = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Outlet id: {self.outlet_id}, stock: {self.instock}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Category name: {self.name}, id: {self.name_id}>'
