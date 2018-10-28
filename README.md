# Find-me-a-house messenger bot

_uses Python 3_

## Installation
```
pip install -r requirements.txt
source crawler-bot-env/bin/activate
```

```
// psql
create database find_me_a_house;
```

## Setup facebook app/page
https://blog.hartleybrody.com/fb-messenger-bot/

## Set the evironment variables
```
FACEBOOK_PAGE_ACCESS_TOKEN=

# Postgres configuration for local use
export FIND_ME_A_HOUSE_DATABASE_NAME='find_me_a_house'
export FIND_ME_A_HOUSE_DATABASE_USER='postgres'
export FIND_ME_A_HOUSE_DATABASE_PASSWORD=
export FIND_ME_A_HOUSE_DATABASE_HOST='localhost'
```

## Example
```bash
# test that it runs
python bot.py --smoke
```

### Arguments
```
  -h, --help      show this help message and exit
  -d, --dry-run   Display the results in terminal but do not actually send
                  them
  -r, --reset     Clean database
  -s, --smoke     Smoke test, verify that it returns a house object
  -f, --facebook  Send message to Facebook Messenger
  -s, --slack     Send message to Slack
```
