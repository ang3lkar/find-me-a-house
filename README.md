# Find-me-a-house messenger bot

## Installation
```
pip install -r requirements.txt
source crawler-bot-env/bin/activate
```

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
```python
python bot.py
```

## Optional arguments
```
  -h, --help      show this help message and exit
  -d, --dry-run   Display the results in terminal but do not actually send
                  them
  -r, --reset     Clean database
  -f, --facebook  Send message to Facebook Messenger
  -s, --slack     Send message to Slack
```
