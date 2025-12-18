from peewee import Model, CharField, DateField, IntegerField
from .db import db

class Product(Model):
    # シフトの日付
    date = DateField()
    # 時間帯 
    name = CharField() 

    class Meta:
        database = db