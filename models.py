import datetime
import os
import peewee
from playhouse.postgres_ext import *

db = PostgresqlExtDatabase(
    os.environ['DATABASE_NAME'],
    user=os.environ['DATABASE_USER'],
    password=os.environ['DATABASE_PASSWORD'],
    host=os.environ['DATABASE_HOST'],
    register_hstore=False
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    sender_id = CharField(unique=True)
    url = TextField(null=True)
    active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


class House(BaseModel):
    user = ForeignKeyField(User)
    title = CharField()
    sys_id = CharField()
    data = JSONField(default={})
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


def get_last_house(user):
    try:
        return House.select().where(House.user == user).order_by(House.created_at.desc()).get()
    except:
        return None

def store_house(user, house):
    House.create(user=user, title=house.title, sys_id=house.sys_id, data=house)

