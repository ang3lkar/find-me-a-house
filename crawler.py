from collections import namedtuple
import urllib
from bs4 import BeautifulSoup

class Crawler:

    def __init__(self, user):
        self.user = user

    def latest(self):
        html = self._get_page(self.user.url)
        doc = BeautifulSoup(html, 'html.parser')

        # Gets first 20 ads
        house_list = doc.find_all('div', {'class': 'lazy'})

        # TODO we want all the latest ones!
        latest_house = house_list[0]

        # struct here
        MyHouse = namedtuple("MyHouse", "link sys_id title location body image_url price area date visits photos agent")

        # Get the details of the latest one!
        link = 'https://xe.gr' + latest_house.select('a')[0].get('href')
        sys_id = link.split("|")[-1].split('.')[0]

        show_home = self._get_page(link)
        show_home_doc = BeautifulSoup(show_home, 'html.parser')

        # Gather all info
        title = latest_house.select('div.r_desc h2 a')[0].text.strip()
        location = latest_house.select('div.r_desc p a')[0].text.strip()
        body = show_home_doc.select('div#d_container p.d.d-google-banner')[0].text.strip()
        image_url = latest_house.select('a img')[0].get('src')
        price = latest_house.select('ul.r_stats li')[0].text.strip()
        area = latest_house.select('ul.r_stats li')[1].text.strip()
        date = latest_house.select('p.r_date')[0].text.strip()
        link = 'https://xe.gr' + latest_house.select('a')[0].get('href')
        #phone = 'https://www.xe.gr/property/phoneimg?sys_id={}'.format(sys_id)
        visits = show_home_doc.select('div.counter strong')[0].text.strip()

        if len(latest_house.select('ul.r_actions li.r_photo')) > 0:
            photos = latest_house.select('ul.r_actions li.r_photo')[0].text.strip()
        else:
            photos = 'x 0'

        if len(latest_house.select('a.pro_action_hotspot')) > 0:
            agent = 'Από μεσίτη'
        else:
            agent = 'Από ιδιώτη'

        return MyHouse(link=link, sys_id=sys_id, title=title, location=location, body=body, image_url=image_url,
                       price=price, area=area, date=date, visits=visits, photos=photos, agent=agent)

    # private

    def _get_page(self, url):
        stream = urllib.request.urlopen(url)
        mybytes = stream.read()
        source = mybytes.decode("utf8")
        stream.close()
        return source
