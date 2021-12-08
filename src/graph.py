from models import Network

def create_json_file(id, node):
	# Get network from id
	g = [each.data for each in Network.query.filter(Network.name == id).all()][0]
	print(g)

	# Get edges linked to nodes:
	edges = list(g.in_edges(node))
	edges.extend(list(g.out_edges(node)))

	node_list = [i[1] for i in edges[:]] + [i[0] for i in edges[:]]

	nodes = [{'id': str(i), 'name': str(i) }  for i in list(set(node_list)) ]
	links = [{'source': u[0], 'target': u[1]} for u in edges ]

	return nodes, links
