''' RUN ONCE TO CREATE THE DATABASE '''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Integer, String, LargeBinary

import networkx as nx
#from models import Networks, Nodes
from pickler import pickle_network

from tqdm import tqdm
import os


app = Flask(__name__)

# SQLAlchemy
db_name = "database.db"

#data_source ="/Users/sdiazdelser/Downloads/networks"

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
                            db.Column('network_id', db.Integer, db.ForeignKey('networks.id')),
                            db.Column('node_id', db.Integer, db.ForeignKey('nodes.id'))
)

# Create database class: Nodes
class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    # many to many relationship:
    which_networks = db.relationship('Networks',
                                     secondary=relationship_table,
                                     backref=db.backref('which_nodes', lazy='dynamic'))
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'

# Create database class: Networks
class Networks(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.LargeBinary())

    def __init__(self, network):
        self.network = network

    def __repr__(self):
        return f'<Network {self.network!r}'




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



'''
    Run app
'''

@app.route('/')

def load_database(data_source="/Users/sdiazdelser/Downloads/networks/tissues"):
    # Find all files in directory
    all_files = list_files(data_source)

    # filter out all non-tsv
    list_tsv= check_tsv(all_files)

    debugger = int(0)

    # add data from each file to database
    for each in tqdm(list_tsv):
        network = add_edgelist(each)

        # pickle network
        pkl_network = pickle_network(network)
        new_network = Networks(pkl_network)

       # pickle nodes
        for node in network.nodes:
            new_node = Nodes(node)

            # add relationship between nodes
            new_network.which_nodes.append(new_node)
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
