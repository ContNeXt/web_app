from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Database settings
db_name = "new_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Assign variable to the db for SQLAlchemy commands
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

if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)