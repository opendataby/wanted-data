from flask import Blueprint, current_app, request, url_for, render_template, abort, jsonify
from markdown import markdown
from sqlalchemy.exc import DatabaseError
from werkzeug.contrib.atom import AtomFeed

from app.db import db, DataSet, Vote


routes = Blueprint(None, __name__)


@routes.route('/')
def index():
    return render_template('index.html', datasets=db.session.query(DataSet).all())


@routes.route('/feed.atom')
def index_feed():
    feed = AtomFeed('wanted opendata.by', feed_url=request.url, url=request.url_root)
    for dataset in db.session.query(DataSet).order_by(DataSet.create.desc()).limit(20).all():
        feed.add(dataset.name, markdown(dataset.description), content_type='html',
                 url=url_for('.dataset', id=dataset.id), published=dataset.create, updated=dataset.create)
    db.session.rollback()
    return feed.get_response()


@routes.route('/dataset/<int:id>')
def dataset(id):
    dataset = db.session.query(DataSet).filter(DataSet.id == id).first()
    if not dataset:
        abort(404)
    return render_template('dataset.html', dataset=dataset)


@routes.route('/dataset/add', methods=['POST'])
def dataset_add():
    name = request.form.get('name')
    description = request.form.get('description')
    if not name:
        current_app.logger.warn('dateset_add: name required')
        return jsonify(status='error', reason='bad value')
    try:
        dataset = DataSet(name, description)
        db.session.add(dataset)
        db.session.commit()
    except DatabaseError as err:
        current_app.logger.warn('dateset_add: error on save', exc_info=err)
        return jsonify(status='error', reason='already exist')
    return jsonify(status='ok', dataset=dataset.id, name=dataset.name)


@routes.route('/dataset/vote', methods=['POST'])
def dataset_vote():
    try:
        email = request.form.get('email')
        dataset_id = int(request.form.get('dataset'))
        dataset = db.session.query(DataSet).filter(DataSet.id == dataset_id).first()
        comment = request.form.get('comment')
        if not email or not dataset:
            raise ValueError
    except ValueError:
        current_app.logger.warn('dateset_vote: email required')
        return jsonify(status='error', reason='bad value')
    try:
        db.session.add(Vote(email, dataset, comment))
        db.session.commit()
    except DatabaseError as err:
        current_app.logger.warn('dateset_vote: error on save', exc_info=err)
        return jsonify(status='error', reason='already exist')
    return jsonify(status='ok', dataset=dataset_id)


@routes.route('/dataset/<int:id>/feed.atom')
def dataset_feed(id):
    dataset = db.session.query(DataSet).filter(DataSet.id == id).first()
    if not dataset:
        abort(404)
    feed = AtomFeed('wanted opendata.by: {}'.format(dataset.name), feed_url=request.url, url=request.url_root)
    for vote in db.session.query(Vote).order_by(Vote.create.desc()).filter(Vote.dataset_id == id).limit(20).all():
        feed.add(dataset.name, markdown(vote.comment), content_type='html',
                 url=url_for('.dataset', id=id), published=vote.create, updated=vote.create)
    db.session.rollback()
    return feed.get_response()
