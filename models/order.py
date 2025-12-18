from peewee import Model, ForeignKeyField, DateTimeField
import datetime
from .db import db
from .user import User
from .product import Product

class Order(Model):
    # 誰が (User)
    user = ForeignKeyField(User, backref='orders')
    # どの枠を (Product)
    product = ForeignKeyField(Product, backref='orders')
    # 提出日時
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db