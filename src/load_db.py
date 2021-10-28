'''

RUN ONCE TO CREATE THE DATABASE

'''

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary

import networkx as nx
#from models import Networks, Nodes
import pickle

from tqdm import tqdm
import os


app = Flask(__name__)

# SQLAlchemy
db_name = "new_database.db"
data_source ="/Users/sdiazdelser/Downloads/networks"

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


'''
database structure 
'''
# Create database class: Nodes
class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(LargeBinary())
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'



# Create database class: Networks
class Networks(db.Model):
    __tablename__ = 'networks'
    id = db.Column(Integer, primary_key=True)
    edge = db.Column(LargeBinary())

    def __init__(self, edge):
        self.edge = edge


'''
For given path, find all tsv files
'''

def list_files(dir):
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

def check_tsv(all_files):
    list_tsv = list()
    for each in all_files:
        # Check the extension
        if each.endswith(".tsv"):
            list_tsv.append(each)
    return list_tsv

def add_edgelist(file_path):
    # Open the file as an nx object
    network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8')
    return network

def pickle_network(network_object):
    # pickle the network objects
    with open('network_database.pkl', 'wb') as network_pickled:
        pickled=pickle.dump(network_object, network_pickled)
        network_pickled.close()
    return pickled

def unpickle_network():
    # unpickle the network objects
    with open('network_database.pkl', 'rb') as network_pickled:
        network_unpickled = pickle.load(network_pickled)
    return network_unpickled


'''
    Run app
'''

@app.route('/')
def load_database(data_source):
    # Find all files in directory
    all_files = list_files(data_source)

    # filter out all non-tsv
    list_tsv= check_tsv(all_files)

    # add data from each file to database
    for each in tqdm(list_tsv):
        network = add_edgelist(each)
        # pickle network
        pkl_edges = pickle_network(list(network.edges))
        pkl_nodes = pickle_network(list(network.nodes))

        new_node = Nodes(pkl_nodes)
        new_edge = Networks(pkl_edges)

        # push to database
        try:
            db.session.add(new_node)
            db.session.add(new_edge)
            db.session.commit()
            return f"<h1> Success! Database created from: {  str(data_source) } </h1>"

        except:
            return "<h1>Something went wrong! Database was not created correctly.</h1>"


if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)
