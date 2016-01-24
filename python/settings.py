import os
import logging

import redis


def get_env():
    if not os.environ.get('ENV'):
        a = os.path.join(os.path.dirname(__file__), '../.env')
        with open(a) as f:
            defaults = dict(tuple(x.strip().split('=')) for x in f.readlines() if x != '\n')
            os.environ.update(defaults)

    return os.environ


env = get_env()

logging.basicConfig(level=getattr(logging, env.get('LOG_LEVEL').upper()))

redis_client = redis.from_url(env.get('REDIS_URL'))

mondo_env = env.get('MONDO_ENV')
mondo_visit_count = env.get('MONDO_VISIT_COUNT')
mondo_account_mapping = dict([env.get('MONDO_ACCOUNT_%s' % i).split(':') for i in range(1, 5)])

foursquare_client_id = env.get('FOURSQUARE_CLIENT_ID')
foursquare_client_secret = env.get('FOURSQUARE_CLIENT_SECRET')
foursquare_api_version = env.get('FOURSQUARE_API_VERSION')

page_url = env.get('PAGE_URL')