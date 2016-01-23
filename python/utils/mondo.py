import requests
import logging


import settings

log = logging.getLogger(__name__)


def post_to_feed(account_id, title, url, image_url):

    headers = {
        'Authorization': 'Bearer %s' % settings.mondo_access_token,
    }

    data = {
        'account_id': account_id,
        'type': 'basic',
        'url': url,
        'params[title]': title,
        'params[image_url]': image_url,
    }

    try:
        result = requests.post('https://staging-api.getmondo.co.uk/feed', data=data, headers=headers).json()
        return result
    except Exception as e:
        log.error(e)
        return None