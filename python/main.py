import json
import logging

from flask import Flask, render_template, request

import settings
from models import Suggestion, Transaction

app = Flask(__name__, template_folder='../html', static_folder='../static')
app.config['DEBUG'] = settings.flask_debug


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
    data = json.loads(request.data.decode('utf8'))

    if data['type'] == 'transaction.created':
        transaction = Transaction(data['data'])
        transaction.save()

        if transaction.visited_count > settings.mondo_visit_count:
            suggestion = transaction.find_suggestion()

            if suggestion:
                suggestion.save()
                suggestion.post_to_feed()

    else:
        log.warning('Unsupported webhook type: %s' % data['type'])

    return ''

if __name__ == "__main__":
    app.run()
