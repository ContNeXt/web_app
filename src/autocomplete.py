# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, SignallingSession
from sqlalchemy import and_
from models import Network, Node, relationship_table

app = Flask(__name__)

# Initialize the database
db = SQLAlchemy(app)

# SQLAlchemy
db_name = "database.db"
session = SignallingSession(db)

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


def query_db_for_nodes(query, context, limit=10):
	"""Return all nodes having the query in their names."""
	# Filter network by context, and nodes in said networks by containing query
	q = db.session.query(Node).join(relationship_table).join(Network).filter(
		and_(Node.name.contains(query), Network.context == context))

	if limit:
		q = q.limit(limit)

	return [each.name for each in q.all()]

