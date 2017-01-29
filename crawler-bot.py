#!/usr/bin/python

import argparse
import os
import pprint
import psycopg2
import requests
import sqlite3
import sys
import urllib.request

from bs4 import BeautifulSoup
from slacker import Slacker

# Setup command line arguments
parser = argparse.ArgumentParser(description='Fetch the latest appartments')
parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                    help='Display the results in terminal but do not send them in Slack')
parser.add_argument(
    '-r', '--reset', default=False, action='store_true', help='Clean database')
args = parser.parse_args()

try:
    url = os.environ['XE_URL']
    token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
except KeyError:
    print('Please set the environment variable XE_URL')
    sys.exit(1)


def get_page(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()
    return html

html = get_page(url)
doc = BeautifulSoup(html, 'html.parser')

# Gets first 20 ads
homes = doc.find_all('div', {'class': 'lazy'})

# We want the latest one
latest_home = homes[0]

# Get the details of the latest one!
link = 'https://xe.gr' + latest_home.select('a')[0].get('href')
sys_id = link.split("|")[-1].split('.')[0]
show_home = get_page(link)
show_home_doc = BeautifulSoup(show_home, 'html.parser')

# Gather all info
title = latest_home.select('div.r_desc h2 a')[0].text
location = latest_home.select('div.r_desc p a')[0].text
body = show_home_doc.select('div#d_container p.d.d-google-banner')[0].text
image_url = latest_home.select('a img')[0].get('src')
price = latest_home.select('ul.r_stats li')[0].text
area = latest_home.select('ul.r_stats li')[1].text
date = latest_home.select('p.r_date')[0].text
link = 'https://xe.gr' + latest_home.select('a')[0].get('href')
# TODO handle binary file to show
phone = 'https://www.xe.gr/property/phoneimg?sys_id={}'.format(sys_id)
visits = show_home_doc.select('div.counter strong')[0].text

if len(latest_home.select('ul.r_actions li.r_photo')) > 0:
    photos = latest_home.select('ul.r_actions li.r_photo')[0].text
else:
    photos = 'x 0'

if len(latest_home.select('a.pro_action_hotspot')) > 0:
    agent = 'Από μεσίτη'
else:
    agent = 'Από ιδιώτη'


# save latest home to DB
con = None
try:
    con = psycopg2.connect(
        host=os.environ['DATABASE_HOST'],
        dbname=os.environ['DATABASE_NAME'],
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASSWORD']
    )
    cur = con.cursor()

    if args.reset:
        cur.execute('DROP TABLE IF EXISTS houses')

    cur.execute('CREATE TABLE IF NOT EXISTS houses (' +
                'id SERIAL PRIMARY KEY' + ',' +
                'sys_id VARCHAR(64)' + ',' +
                'title VARCHAR(128)' + ',' +
                'data JSON' + ',' +
                'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)'
                )
    con.commit()

    cur.execute('SELECT sys_id FROM houses ORDER BY created_at DESC LIMIT 1')
    row = cur.fetchone()

    if row is None:
        data = (sys_id, title)
        cur.execute("INSERT INTO houses(sys_id, title) VALUES (%s, %s);", data)
        con.commit()

    else:
        if row[0] == sys_id:
            print(
                'House \'{title}\' already exists in database'.format(title=title))
        else:
            data = (sys_id, title)
            cur.execute(
                "INSERT INTO houses(sys_id, title) VALUES (%s, %s);", data)
            con.commit()
            print("New house in database: %s" % cur.lastrowid)

except sqlite3.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)

finally:
    if con:
        con.close()


if args.dry_run:
    print('Dry mode enabled, message to slack ignored.')

else:
    # SLACK
    # home_attachment = {
    #     #"author_name": "Χρυσή ευκαιρία",
    #     "color": "#36a64f",
    #     "title": "{title} ({price})".format(title=title, price=price),
    #     "title_link": link,
    #     "text": "{body}\n\nPhone link: {phone}".format(body=body, phone=phone),
    #     "image_url": link,
    #     "thumb_url": image_url,
    #     "footer": "{v} επισκέψεις | {n} φωτογραφίες | {s}".format(v=visits, n=photos, s=agent)
    # }
    # # Send a message to me
    # print('Sending ad to Slack...')
    # pprint.pprint(home_attachment)
    # slack = Slacker(os.environ['SLACK_TOKEN'])
    # slack.chat.post_message(
    #     '@angelos', 'Νέα αγγελία από Χρυσή ευκαιρία!', attachments=[home_attachment])

    # FACEBOOK
    image_payload = {
      "recipient":{
        "id":"1198499103580071"
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
               {
                "title": location,
                "image_url": image_url,
                "subtitle": "{title} ({price})".format(title=title, price=price),
                "default_action": {
                  "type": "web_url",
                  "url": link,
                  "messenger_extensions": False,
                  "webview_height_ratio": "tall"
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url": link,
                    "title":"View Details"
                  }
                ]
              }
            ]
          }
        }
      }
    }
    r1 = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=image_payload)

    payload = {
        "message": {
            "text": body
        },
        "recipient": {
            "id": "1198499103580071"
        }
    }

    r2 = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
