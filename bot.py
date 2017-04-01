#!/usr/bin/python

import arguments
import models
from client import Client
from crawler import Crawler

ARGS = arguments.get()

DB = models.db
DB.connect()


if ARGS.reset:
    print('Dropping tables')
    models.House.drop_table()
    models.User.drop_table()


if not models.User.table_exists():
    print('No tables found, creating db schema')
    DB.create_tables([models.User, models.House])


for user in models.User.select().where(models.User.active == True):
    print('Crawling for {name}'.format(name=user.name))

    house = Crawler(user).latest()
    last_house = models.get_last_house(user)

    if ARGS.dry_run:
        print(house)
        exit(0)

    if (last_house is None) or (house.sys_id != last_house.sys_id):
        models.store_house(user, house)
        Client('facebook').send(user, house)
    else:
        print('No new houses')
