# home-ads-bot

## Install and activate packages
```
pip install -r requirements.txt
source crawler-bot-env/bin/activate
```

## Set the evironment variables
```
XE_URL=
SLACK_TOKEN=
FACEBOOK_PAGE_ACCESS_TOKEN=

# Postgres configuration
DATABASE_HOST=
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
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
