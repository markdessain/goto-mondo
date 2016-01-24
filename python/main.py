import json
import logging
import datetime

from flask import Flask, render_template, request
from settings import redis_client, mondo_visit_count, page_url

from utils import foursquare
from utils import mondo
from models import Suggestion

app = Flask(__name__, template_folder='../html', static_folder='../static')
app.config['DEBUG'] = True


log = logging.getLogger(__name__)


@app.route('/')
def route_index():
    return render_template('index.html')


@app.route('/suggestion/<suggestion_id>')
def route_suggestion(suggestion_id):
    suggestion = Suggestion.get(suggestion_id)
    return render_template('suggestion.html', suggestion=suggestion)


@app.route('/webhook', methods=['POST'])
def route_webhook():
    transaction = json.loads(request.data.decode('utf8'))

    if not transaction['data']['is_load']:

        merchant = transaction['data']['merchant']
        account_id = transaction['data']['account_id']

        date = datetime.date.today()
        year_and_week = "%s_%s" % (date.isocalendar()[1], date.year)

        redis_key = "%s_%s_%s" % (account_id, merchant['id'], year_and_week)
        redis_client.incr(redis_key, 1)

        current_count = redis_client.get(redis_key)
        if int(current_count) > int(mondo_visit_count):
            name = merchant['name']
            body = "You've already been to %s %s times this week. Why try here instead?" % (name, int(current_count))
            long = merchant['address']['longitude']
            lat = merchant['address']['latitude']

            venue_id = foursquare.get_venue_id(name, lat, long)

            if venue_id:
                similar_venues = foursquare.get_similar_venues(venue_id)

                if similar_venues['items']:
                    new_name = similar_venues['items'][0]['name']
                    title = 'Try %s next time?' % new_name
                    image_url = similar_venues['items'][0]['categories'][0]['icon']['prefix'] + 'bg_64' + similar_venues['items'][0]['categories'][0]['icon']['suffix']

                    suggestion_id = Suggestion(new_name, name, current_count).save()
                    url = '%s/suggestion/%s' % (page_url, suggestion_id)
                    mondo.post_to_feed(account_id, title, body, url, image_url)
                else:
                    log.info('Nothing Similar')
            else:
                log.info('Could not find the venue')
        else:
            log.info('Only been once')
    else:
        log.info('Mondo Top up')

    return ''


if __name__ == "__main__":
    app.run()

