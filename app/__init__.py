import logging

from flask import Flask
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
