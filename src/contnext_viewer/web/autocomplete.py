# -*- coding: utf-8 -*-
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from contnext_viewer.models import Network, Node, relationship_table, engine

def autocomplete_search(query, context, limit=10):
	# Start database session
	Session = sessionmaker(bind=engine)
	sqlsession = Session()

	"""Return all nodes having the query in their names."""
	# Filter network by context, and nodes in said networks by containing query
	q = sqlsession.query(Node).join(relationship_table).join(Network).filter(
		and_(Node.name.contains(query), Network.context == context))
	if limit:
		q = q.limit(limit)

	return [each.name for each in q.all()]

