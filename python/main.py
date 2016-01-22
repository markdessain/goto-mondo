import logging

from flask import Flask, render_template, jsonify


app = Flask(__name__, template_folder='../html', static_folder='../static')
app.config['DEBUG'] = True


log = logging.getLogger(__name__)


@app.route('/')
def route_index():
    return render_template('index.html')

