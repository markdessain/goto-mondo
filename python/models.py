import json

from utils.strings import random_string
from settings import redis_client


class Suggestion(object):

    def __init__(self, name, replacement, count):
        self.name = name
        self.replacement = replacement
        self.count = count

    def save(self):
        name = random_string()
        redis_client.set('suggestion:%s' % name, json.dumps({'name': self.name, 'replacement': self.replacement, 'count': int(self.count) }))
        return name

    @staticmethod
    def get(name):
        values = json.loads(redis_client.get('suggestion:%s' % name).decode('utf-8'))
        return Suggestion(**values)