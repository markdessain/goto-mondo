import json
import logging
import datetime

import settings
from utils import mondo
from utils import foursquare
from settings import redis_client
from utils.strings import random_string


log = logging.getLogger(__name__)


class Model(object):
    pass


class Suggestion(Model):

    def __init__(self, account_id, image_url, name, replacement, count):
        self.account_id = account_id
        self.image_url = image_url
        self.name = name
        self.replacement = replacement
        self.count = int(count)
        self.redis_key = ''

    def save(self):
        redis_key = 'suggestion:%s' % random_string()
        data = {
            'account_id': self.account_id,
            'image_url': self.image_url,
            'name': self.name,
            'replacement': self.replacement,
            'count': self.count,
        }
        redis_client.set(redis_key, json.dumps(data))
        self.redis_key = redis_key

    @staticmethod
    def get(redis_key):
        values = json.loads(redis_client.get(redis_key).decode('utf-8'))
        return Suggestion(**values)

    def post_to_feed(self):
        title = 'Try %s next time?' % self.name
        body = "You've already been to %s %s times this week. Why try here instead?" % (self.replacement, self.count)

        url = '%s/suggestion/%s' % (settings.page_url, self.redis_key)
        mondo.post_to_feed(self.account_id, title, body, url, self.image_url)


class Transaction(Model):

    def __init__(self, data):
        self.data = data
        self.redis_key = ''

    def save(self):
        merchant = self.data['merchant']
        account_id = self.data['account_id']

        date = datetime.date.today()
        year_and_week = '%s_%s' % (date.isocalendar()[1], date.year)

        redis_key = '%s_%s_%s' % (account_id, merchant['id'], year_and_week)
        redis_client.incr(redis_key, 1)

        self.redis_key = redis_key

    @property
    def visited_count(self):
        return int(redis_client.get(self.redis_key))

    def find_suggestion(self):
        merchant = self.data['merchant']
        account_id = self.data['account_id']

        name = merchant['name']
        long = merchant['address']['longitude']
        lat = merchant['address']['latitude']

        venue_id = foursquare.get_venue_id(name, lat, long)

        if venue_id:
            similar_venues = foursquare.get_similar_venues(venue_id)

            if similar_venues['items']:
                new_name = similar_venues['items'][0]['name']
                image_url = similar_venues['items'][0]['categories'][0]['icon']['prefix'] + 'bg_64' + similar_venues['items'][0]['categories'][0]['icon']['suffix']

                return Suggestion(account_id, image_url, new_name, name, self.visited_count)
            else:
                log.info('No suggestion available')
        else:
            log.info('Could not find the venue')
