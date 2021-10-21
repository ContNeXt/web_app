'''

RUN ONCE TO CREATE THE DATABASE

'''

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import networkx as nx
# from models import Networks, Nodes

from tqdm import tqdm
import os


app = Flask(__name__)

# SQLAlchemy
db_name = "testDatabase.db"
data_source ="networks"

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    #neighbours = db.relationship('Networks', backref='node', lazy=True)
    def __init__(self, name):
        self.name = name



# Create database class: Networks
class Networks(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    # net_id= db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    geneStart = db.Column(db.String(20), nullable=False)
    geneEnd = db.Column(db.String(20), nullable=False)
    direction = db.Column(db.String(20), nullable=True, default='0')
    method = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(200), nullable=False)

    def __init__(self, geneStart, geneEnd, direction, method, weight):
        self.geneStart = geneStart
        self.geneEnd = geneEnd
        self.direction = direction
        self.method = method
        self.weight = weight



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
            allFiles = all_files + list_files(full_path)
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
def load_database(data_source="/Users/sdiazdelser/Downloads/networks"):
    # Find all files in directory
    all_files = list_files(data_source)

    # filter out all non-tsv
    list_tsv= check_tsv(all_files)

    sources = list()
    # add data from each file to database
    try:
        for each in tqdm(list_tsv):
            network = add_edgelist(each)
            new_node = Nodes(list(network.nodes))
            new_network = Networks(list(network.edges))

            # to make sure it's working
            sources.append(network)
            #db.session.add(new_node)
            #db.session.add(new_network)
            #db.session.commit()
        return f"<h1> Success! Database created from: { str(sources) } </h1>"

    except:
        return "<h1>Something went wrong! Database was not created correctly.</h1>"


if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)
