from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class DataSet(db.Model):

    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True)
    create = Column(DateTime, default=datetime.utcnow)
    name = Column(String(80), unique=True)
    description = Column(String(800))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Vote(db.Model):

    __tablename__ = 'vote'

    id = Column(Integer, primary_key=True)
    create = Column(DateTime, default=datetime.utcnow)
    email = Column(String(64))
    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    dataset = relationship('DataSet', backref='votes', order_by='Vote.create')
    subsribe = Column(String(1))
    comment = Column(String(160))

    __table_args__ = (
         UniqueConstraint('dataset_id', 'email'),
    )

    def __init__(self, email, dataset, comment):
        self.email = email
        self.dataset = dataset
        self.comment = comment
