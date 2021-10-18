'''

RUN ONCE TO CREATE THE DATABASE

'''

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
from tqdm import tqdm
import os


app = Flask(__name__)

# SQLAlchemy
db_name = "testDatabase.db"
data_source ="networks2"

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)



'''
Function loads data from given tsv file into database1.db
!!!!! ATTENTION: currently set to csv, instead !!!!!
'''

def loadDatabase(tsv_file):
    # Open tsv file
    with open(tsv_file) as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row:
                new = Networks(geneStart=row[0],
                              geneEnd=row[1],
                              direction=row[2],
                              method=row[3],
                              weight=row[4],
                              )
                # Push to Database
                db.session.add(new)
                db.session.commit()
    source = tsv_file
    return source

'''
For given path, find all tsv files
'''

def list_files(dir):
    # create a list of file and sub directories
    listOfFile = os.listdir(dir)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dir, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + list_files(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def check_tsv(allFiles):
    list_tsv = list()
    for each in allFiles:
        # Check the extension
        if each.endswith(".csv"):
            list_tsv.append(each)
    return list_tsv



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
    # node_id= db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    # !!!! need to make node_id a list.
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
    Run app
'''

@app.route('/')
def testdb():
    # Load data
    # Find all files in directory
    allFiles = list_files(data_source)
    # filter out all non-tsv
    list_tsv= check_tsv(allFiles)

    # add data from each file to database
    sources = list()
    try:
        for each in tqdm(list_tsv):
            source = loadDatabase(each)
            sources.append(source)
        return f"<h1> Success! Database created from: { str(sources) } </h1>"

    except:
        return "<h1>Something went wrong! Database was not created correctly.</h1>"



if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)
