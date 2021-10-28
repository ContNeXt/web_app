""" RUN ONCE TO CREATE THE DATABASE """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Integer, String, LargeBinary

import networkx as nx
from models import Network, Node
from pickler import pickle_network

from tqdm import tqdm
import os


app = Flask(__name__)

# SQLAlchemy
db_name = "database_2.db"

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


""""
# Create database class: Network
class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    data = db.Column(db.PickleType())
    # many-to-many relationship
    _nodes = db.relationship('Node',
                             secondary=relationship_table,
                             lazy='dynamic',
                             backref=db.backref('node_to_network_table_backref'))

    def __init__(self, data, name):
        self.data = data
        self.name = name

    def __repr__(self):
        return f'<Network {self.data!r}'
        return f'<Network {self.name!r}'

# Create database class: Node
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    # many to many relationship:
    _networks = db.relationship('Network',
                                     secondary=relationship_table,
                                     lazy='dynamic',
                                     backref=db.backref('nodes'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'


"""
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


def files_to_dic(all_files):
    """ Create dictionary of network names and files"""
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
            print("deleting: ",each[0])
            del all_files_dic[each[0]]
    return all_files_dic

def add_edgelist(file_path):
    # Open the file as an nx object
    network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8', create_using=nx.DiGraph())
    return network



'''
    Run app
'''

@app.route('/')

def load_database(data_source ="/Users/sdiazdelser/Downloads/networks2/tissues"):
    # Find all files
    all_files = list_files(data_source)
    dic = files_to_dic(all_files)

    # filter out all non-tsv
    list_tsv= check_tsv(dic)

    # counter
    debugger = int(0)

    # add data from each file to database
    for key, value in tqdm(list_tsv.items()):
        network = add_edgelist(value)
        new_network = Network(name=key, data=network)

        # pickle network -> NOT NEEDED if we add it as a pickled object
        # pkl_network = pickle_network(network)
        # new_network = Network(name=key, data=pkl_network )

        for node in network.nodes:
            new_node = Node(name=node)

            # add relationship between nodes
            new_network._nodes.append(new_node)
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
