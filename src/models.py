from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Database settings
db_name = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Assign variable to the db for SQLAlchemy commands
db = SQLAlchemy(app)

'''
database structure 
'''

# Create many-to-many relationship table
networks=db.Table('relationship_table',
                            db.Column('network_id', db.Integer, db.ForeignKey('network.id'), primary_key=True),
                            db.Column('node_id', db.Integer, db.ForeignKey('node.id'), primary_key=True)
)


# Create database class: Node
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    # many to many relationship:
    networks = db.relationship('Networks',
                                     secondary=networks,
                                     lazy='dynamic',
                                     backref=db.backref('nodes'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Node {self.name!r}'

# Create database class: Network
class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.PickleType())


    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'<Network {self.data!r}'

if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)