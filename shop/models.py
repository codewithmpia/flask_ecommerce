from datetime import datetime
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from .settings import db 


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)
    orders = db.relationship("Order", backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password2):
        return check_password_hash(self.password, password2)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    products = db.relationship("Product", backref="category")

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.generate_slug()
        
    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
        else:
            self.slug = ""

    def __str__(self):
        return self.name

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer(), primary_key=True)
    category_id = db.Column(db.Integer(), db.ForeignKey("categories.id"))
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text(), nullable=False)
    image1 = db.Column(db.Unicode(128))
    image2 = db.Column(db.Unicode(128))
    image3 = db.Column(db.Unicode(128))
    price = db.Column(db.Float())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
    available = db.Column(db.Boolean(), default=True)
    orders = db.relationship("Order", backref="product")
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.generate_slug()
        
    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
        else:
            self.slug = ""

    @property
    def get_absolute_url(self):
        return ""
    
    def __str__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer(), db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer(), nullable=False)
    total = db.Column(db.Float())
    date = db.Column(db.DateTime(), default=datetime.now())

    

    

