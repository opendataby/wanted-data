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
app.logger.setLevel(logging.INFO)


@app.before_request
def before_request():
    if any(re.match(re.escape(ip).replace('\*', '\d+'), request.remote_addr)
           for ip in os.environ.get('BAN_IPS', '').split(',')):
        abort(403)
