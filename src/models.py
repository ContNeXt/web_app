from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base

'''
database structure 
'''
# Create database class: Nodes
class Nodes(Base):
    __tablename__ = 'nodes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(LargeBinary())
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'



# Create database class: Networks
class Networks(Base):
    __tablename__ = 'networks'
    id = db.Column(Integer, primary_key=True)
    edge = db.Column(LargeBinary())

    def __init__(self, geneStart, geneEnd, direction, method, weight):
        self.geneStart = geneStart
        self.geneEnd = geneEnd
        self.direction = direction
        self.method = method
        self.weight = weight
