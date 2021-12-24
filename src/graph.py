from models import Network


def create_json_file(id, node):
	# Get network from id
	try:
		g = [each.data for each in Network.query.filter(Network.identifier == id).all()][0]
		properties = [each.properties for each in Network.query.filter(Network.identifier == id).all()][0]
	except:
		return [], []

	# Get edges linked to nodes:
	edges = list(g.edges(node))

	node_list = list(set([i[1] for i in edges[:]] + [i[0] for i in edges[:]]))
	nodes_dic = {node_list[i]: i for i in range(len(node_list))}

	nodes = [{'id': nodes_dic[str(i)], 'name': str(i), 'connections': properties.get(i).get('connections'),
				'rank': properties.get(i).get('rank'), 'housekeeping': properties.get(i).get('housekeeping')
				} for i in list(set(node_list))]
	links = [{'source': nodes_dic[u[0]], 'target': nodes_dic[u[1]]} for u in edges]
	return nodes, links
