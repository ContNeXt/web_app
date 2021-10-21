from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import Column, Integer, String
from app.database import Base

'''
database structure 
'''
# Create database class: Nodes
class Nodes(Base):
    __tablename__ = 'nodes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(20), nullable=False)
    #neighbours = db.relationship('Networks', backref='node', lazy=True)
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'



# Create database class: Networks
class Networks(Base):
    __tablename__ = 'networks'
    id = db.Column(Integer, primary_key=True)
    # net_id= db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    # !!!! need to make node_id a list.
    geneStart = db.Column(String(20), nullable=False)
    geneEnd = db.Column(String(20), nullable=False)
    direction = db.Column(String(20), nullable=True, default='0')
    method = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(200), nullable=False)

    def __init__(self, geneStart, geneEnd, direction, method, weight):
        self.geneStart = geneStart
        self.geneEnd = geneEnd
        self.direction = direction
        self.method = method
        self.weight = weight
