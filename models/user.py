from peewee import Model, CharField
from .db import db

class User(Model):
    # スタッフ名
    name = CharField()
    # 性別（集計グラフ用）
    gender = CharField(null=True)

    class Meta:
        database = db