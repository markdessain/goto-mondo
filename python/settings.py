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

redis_client = redis.Redis(env.get('REDIS_HOST'), port=int(env.get('REDIS_PORT')), decode_responses=True)

mondo_access_token = env.get('MONDO_ACCESS_TOKEN')
mondo_account_id = env.get('MONDO_ACCOUNT_ID')

foursquare_client_id = env.get('FOURSQUARE_CLIENT_ID')
foursquare_client_secret = env.get('FOURSQUARE_CLIENT_SECRET')
foursquare_api_version = env.get('FOURSQUARE_API_VERSION')

