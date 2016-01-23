import settings
import requests

import logging


log = logging.getLogger(__name__)


def get_venue_id(merchant_name, lat, long):

    params = {
        'query': merchant_name,
        'll': '%s,%s' % (lat, long),
        'radius': 100,
        'client_id': settings.foursquare_client_id,
        'client_secret': settings.foursquare_client_secret,
        'intent': 'checkin',
        'limit': 1,
        'v': settings.foursquare_api_version
    }

    try:
        result = requests.get('https://api.foursquare.com/v2/venues/search', params=params).json()['response']['venues'][0]['id']
        return result
    except Exception as e:
        log.error(e)
        return []


def get_next_venues(venue_id):

    params = {
        'client_id': settings.foursquare_client_id,
        'client_secret': settings.foursquare_client_secret,
        'v': settings.foursquare_api_version
    }

    try:
        result = requests.get('https://api.foursquare.com/v2/venues/%s/nextvenues' % venue_id, params=params).json()['response']['nextVenues']
        return result
    except Exception as e:
        log.error(e)
        return []


def get_similar_venues(venue_id):

    params = {
        'client_id': settings.foursquare_client_id,
        'client_secret': settings.foursquare_client_secret,
        'v': settings.foursquare_api_version
    }

    try:
        result = requests.get('https://api.foursquare.com/v2/venues/%s/similar' % venue_id, params=params).json()['response']['similarVenues']
        return result
    except Exception as e:
        log.error(e)
        return []



#
# long = -0.0880558
# lat = 51.5262576
# name = 'Starbucks'
#
# venue_id = get_venue_id(name, lat, long)
# print(venue_id)
# similar = get_similar_venues(venue_id)
# next = get_next_venues(venue_id)
# print(similar)
# print(next)