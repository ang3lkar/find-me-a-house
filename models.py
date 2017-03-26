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
    sender_id = IntegerField(unique=True)
    url = TextField()
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

