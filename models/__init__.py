from peewee import SqliteDatabase
from .db import db
from .user import User
from .product import Product
from .order import Order

MODELS = [User, Product, Order]

def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()