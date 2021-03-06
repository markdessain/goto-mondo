import requests
import logging


import settings

log = logging.getLogger(__name__)


def post_to_feed(account_id, title, body, url, image_url):

    headers = {
        'Authorization': 'Bearer %s' % settings.mondo_account_mapping.get(account_id),
    }

    data = {
        'account_id': account_id,
        'type': 'basic',
        'url': url,
        'params[title]': title,
        'params[image_url]': image_url,
        'params[body]': body
    }

    try:
        result = requests.post('%s/feed' % settings.mondo_env, data=data, headers=headers).json()
        return result
    except Exception as e:
        log.error(e)
        return None
