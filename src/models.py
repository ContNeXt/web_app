# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, PickleType, ForeignKey, Table
from pathlib import Path
from sqlalchemy.orm import relationship, backref

# SQLAlchemy
DB_PATH = str(Path(Path(__file__).parent.resolve(), 'contnext.db'))

# Create engine
engine = create_engine('sqlite:///'+DB_PATH)
Base = declarative_base()

'''
database structure 
'''

# Create many-to-many relationship table
relationship_table=Table('relationship_table',
                         Base.metadata,
                         Column('network_id', Integer, ForeignKey('network.id'), primary_key=True),
                         Column('node_id', Integer, ForeignKey('node.id'), primary_key=True)
)

# Create database class: Network
class Network(Base):
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    data = Column(PickleType())
    context = Column(String(30))
    identifier = Column(String(50), unique=True)
    properties = Column(PickleType)

    # many-to-many relationship
    nodes_ = relationship('Node',
                             secondary=relationship_table,
                             lazy='dynamic',
                             backref=backref('networks_'))

    def __init__(self, data, name, context, identifier, properties):
        self.data = data
        self.name = name
        self.context = context
        self.identifier = identifier
        self.properties = properties

    def __repr__(self):
        return f'<Network {self.data!r}'


# Create database class: Node
class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'

Base.metadata.create_all(engine, checkfirst=True)
