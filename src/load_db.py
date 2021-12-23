# -*- coding: utf-8 -*-

""" RUN ONCE TO CREATE THE DATABASE """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
import networkx as nx
# from models import Network, Node, relationship_table

from typing import List, Tuple
from tqdm import tqdm
import os
import sys
import csv
from pathlib import Path


app = Flask(__name__)

# SQLAlchemy
DB_NAME = "contnext.db"
# TODO make database in hidden folder in home dir
HIDDEN_FOLDER = os.path.join(Path.home(), '.contnext')
DB_PATH = os.path.join(HIDDEN_FOLDER, DB_NAME)
DATA_SOURCE = sys.argv[1]


app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Initialize the database
db = SQLAlchemy(app)

'''
database structure 
'''

# Create many-to-many relationship table
relationship_table=db.Table('relationship_table',
                            db.Column('network_id', db.Integer, db.ForeignKey('network.id'), primary_key=True),
                            db.Column('node_id', db.Integer, db.ForeignKey('node.id'), primary_key=True)
)

# Create database class: Network
class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.PickleType())
    context = db.Column(db.String(30))
    identifier = db.Column(db.String(50), unique=True)

    # many-to-many relationship
    nodes_ = db.relationship('Node',
                             secondary=relationship_table,
                             lazy='dynamic',
                             backref=db.backref('networks_'))

    def __init__(self, data, name, context, identifier):
        self.data = data
        self.name = name
        self.context = context
        self.identifier = identifier

    def __repr__(self):
        return f'<Network {self.data!r}'


# Create database class: Node
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'


def list_files(dir:str) -> List:
    """ List all the files in a directory and it's sub-directories """
    # create a list of file and sub directories
    list_of_files = os.listdir(dir)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + list_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def check_tsv(all_files: List) -> Tuple[List, List]:
    """ Filters out all non-tsv files from the dictionary"""
    node_degree = []
    supplementary = []
    all_tsv_files = []
    for file in all_files[:]:
        # Check the extension
        if not file.endswith(".tsv"):
            continue
        elif file.endswith("overview.tsv"):
            # add to supplementary list
            supplementary.append(file)
            continue
        elif file.endswith("degree.tsv"):
            # add degree to list
            node_degree.append(file)
            continue
        elif file.endswith("Readme.tsv"):
            continue
        all_tsv_files.append(file)
    return all_tsv_files, supplementary


def create_node_set(list_tsv):
    """ Create a set of all the nodes """
    # init set of nodes
    list_of_nodes = set()
    # get a set of nodes
    for value in tqdm(list_tsv.values()):
        for node in value.nodes:
            list_of_nodes.add(node)
    return list_of_nodes


def add_edgelist(file_path, interacFlag=False):
    """ Create networkx edgelist from file"""
    # Open the file as an nx object
    if interacFlag:
        network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8', create_using=nx.DiGraph())
        return network

    network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8', create_using=nx.Graph())
    return network


def add_metadata_to_networks(supplementary_files: List):
    """ Add metadata to networks from list of supplementary tsv files, """
    network_metadata = {}
    for file in supplementary_files:
        with open(file, 'r') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            header = next(csv_reader) # skip header
            for row in csv_reader:
                network_metadata.update({row[0].split(":")[1]: {'context': os.path.basename(os.path.dirname(file)),
                                                                'id': row[0],
                                                                'name': row[1]}
                                         })
    return network_metadata

'''
    Run app
'''

@app.route('/')
def load_database(data_source=DATA_SOURCE):
    """ Load the SQL-Alchemy Database with files from given directory """

    if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        return f"<h1> Database already exists: {str('sqlite:///' + DB_NAME)} </h1>"

    # Find all files
    all_files = list_files(data_source)
    # filter out all non-tsv, and get supplementary dict
    list_tsv, supplementary_source = check_tsv(all_files=all_files)

    # counter
    debugger = int(0)
    # init list of nodes
    list_of_nodes = []

    metadata = add_metadata_to_networks(supplementary_files=supplementary_source)

    # add data from each file to database
    for file in tqdm(list_tsv, total=len(list_tsv)):
        key = os.path.basename(os.path.dirname(file))
        new_network = Network(identifier=metadata.get(key).get('id'),
                              data=add_edgelist(file),
                              context=metadata.get(key).get('context'),
                              name=metadata.get(key).get('name'))

        for node in add_edgelist(file).nodes:
            # check if node is already in the database
            q = Node.query.filter(Node.name == node).first()
            if q:
                new_node = q
            else:
                new_node = Node(name=node)
                list_of_nodes.append({'node': node})
            # add relationship between nodes
            new_network.nodes_.append(new_node)
            db.session.add(new_node)

        debugger = debugger+1

        # push to database
        db.session.add(new_network)
        db.session.commit()

    return f"<h1> Files uploaded to database: {str(debugger) } </h1>"



if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)
