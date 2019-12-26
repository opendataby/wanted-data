import logging
import re

from flask import Flask, request, abort
from flaskext.markdown import Markdown

from app.db import db, DataSet, Vote
from app.route import routes


app = Flask(__name__)
app.config.from_object('app.settings')
Markdown(app)

db.init_app(app)
db.app = app
db.create_all()
app.register_blueprint(routes)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(app.config['LOG_LEVEL'])


@app.before_request
def before_request():
    for ip in app.config['BAN_IPS']:
        ip_pattern = re.escape(ip).replace(r'\*', r'\d+')
        if re.match(ip_pattern, request.access_route[-1]):
            app.logger.info('BAN_IPS matched %s', ip)
            abort(403)
