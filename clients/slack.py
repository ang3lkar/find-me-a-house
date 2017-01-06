from slacker import Slacker

def send(house):

    try:
        token = os.environ['SLACK_TOKEN']
    except KeyError:
        print('Please set the environment variable SLACK_TOKEN')
        sys.exit(1)

    home_attachment = {
        #"author_name": "Χρυσή ευκαιρία",
        "color": "#36a64f",
        "title": "{title} ({price})".format(title=title, price=price),
        "title_link": link,
        "text": "{body}\n\nPhone link: {phone}".format(body=body, phone=phone),
        "image_url": link,
        "thumb_url": image_url,
        "footer": "{v} επισκέψεις | {n} φωτογραφίες | {s}".format(v=visits, n=photos, s=agent)
    }
    # Send a message to me
    print('Sending ad to Slack...')

    slack = Slacker(token)
    slack.chat.post_message('@angelos', 'Νέα αγγελία από Χρυσή ευκαιρία!', attachments=[home_attachment])

