from peewee import Model, CharField, IntegerField
from .db import db

class Product(Model):
    name = CharField()
    price = IntegerField()

    class Meta:
        database = db