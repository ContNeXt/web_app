# -*- coding: utf-8 -*-

""" RUN ONCE TO CREATE THE DATABASE """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import networkx as nx
import csv
#from models import Network, Node, relationship_table

from tqdm import tqdm
import os
import sys

app = Flask(__name__)

# SQLAlchemy
db_name = "database.db"
data_source = sys.argv[1]
#data_source= "/../../Downloads/networks2"

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
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
    name = db.Column(db.String(40), unique=True)
    data = db.Column(db.PickleType())
    context = db.Column(db.String(30))
    context_info = db.Column(db.String(50))

    # many-to-many relationship
    nodes_ = db.relationship('Node',
                             secondary=relationship_table,
                             lazy='dynamic',
                             backref=db.backref('networks_'))

    def __init__(self, data, name, context, context_info):
        self.data = data
        self.name = name
        self.context = context
        self.context_info = context_info

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


'''
For given path, find all tsv files
'''

def list_files(dir):
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


def files_to_dic(all_files):
    """ Create dictionary of network id and files"""
    # init dic
    all_files_dic = {}
    # iterate over all files
    for files in all_files:
        dirpath = os.path.dirname(files)
        # Add to dictionary
        all_files_dic.update({os.path.basename(dirpath): files})
    return all_files_dic


def check_tsv(all_files_dic):
    """ Filters out all non-tsv files from the dictionary"""
    for each in list(all_files_dic.items()):
        # Check the extension
        if not each[1].endswith(".tsv"):
            del all_files_dic[each[0]]
    return all_files_dic

def create_node_set(list_tsv):
    """ Create a set of all the nodes """
    # init set of nodes
    list_of_nodes = set()
    # get a set of nodes
    for value in tqdm(list_tsv.values()):
        for node in value.nodes:
            list_of_nodes.add(node)
    return list_of_nodes

def add_edgelist(file_path):
    """ Create networkx edgelist from file"""
    # Open the file as an nx object
    network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8', create_using=nx.DiGraph())
    return network

def add_metadata_to_networks(file_path: str):
    """ Add metadata to networks from tsv file, """
    metadata_dict = {}
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        header = next(csv_reader) # skip header
        for row in csv_reader:
            metadata_dict.update({row[0].split(":")[1]: row[1]})
    return metadata_dict

def get_context(file:str) -> str:
    """Get context from data folder structure"""
    # structure is: context/network_name/file.tsv
    dir = os.path.dirname(os.path.dirname(file))
    return os.path.basename(dir)

'''
    Run app
'''

@app.route('/')
def load_database(data_source=data_source):
    """ Load the SQL-Alchemy Database with files from given directory """
    SUPPLEMENTARY_SOURCE = os.path.join(data_source, 'ContNeXt supplementary - Tissue overview.tsv')
    # Find all files
    all_files = list_files(data_source)
    dic = files_to_dic(all_files)

    # filter out all non-tsv
    list_tsv = check_tsv(dic)

    # counter
    debugger = int(0)
    # init list of nodes
    list_of_nodes = []

    context_info = add_metadata_to_networks(file_path=SUPPLEMENTARY_SOURCE)
    # add data from each file to database
    for key, value in tqdm(list_tsv.items()):
        new_network = Network(name=key, data=add_edgelist(value), context=get_context(value), context_info=context_info.get(key, None))

        for node in add_edgelist(value).nodes:
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
