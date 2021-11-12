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

    # many-to-many relationship
    _nodes = db.relationship('Node',
                             secondary=relationship_table,
                             lazy='dynamic',
                             backref=db.backref('node_to_network_table_backref'))

    def __init__(self, data, name, context, _nodes):
        self.data = data
        self.name = name
        self._nodes = _nodes
        self.context = context

    def __repr__(self):
        return f'<Network {self.data!r}'

# Create database class: Node
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    context = db.Column(db.String(30))
    # many-to-many relationship:
    _networks = db.relationship('Network',
                                     secondary=relationship_table,
                                     lazy='dynamic',
                                     backref=db.backref('nodes'))

    def __init__(self, name, context, _networks):
        self.name = name
        self.context = context
        self._networks = _networks

    def __repr__(self):
        return f'<Node {self.name!r}'


if __name__ == "__main__":

    # Create database
    db.create_all()
    db.session.commit()
    app.run(debug=True)