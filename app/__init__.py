import logging
import os
import re

from flask import Flask, request, abort
from flask.ext.markdown import Markdown

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
app.logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))


@app.before_request
def before_request():
    banned = os.environ.get('BAN_IPS', '').split(',')
    for ip in banned:
        ipre = re.escape(ip).replace('\*', '\d+')
        app.logger.debug(f'access_route: {request.access_route}')
        app.logger.debug(f'ipre: {ipre}')
        if re.match(ipre, request.access_route[-1]):
            app.logger.info(f'BAN_IPS matched {ip}')
            abort(403)
