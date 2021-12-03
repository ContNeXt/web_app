import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from sqlalchemy import and_
from models import Network, Node, relationship_table

def create_json_file(g, node):
	FILENAME = str(node) + '.json'

	# Get edges linked to nodes:
	edges = list(g.in_edges(node))
	edges.extend(list(g.out_edges(node)))

	node_list = [i[1] for i in edges[:]] + [i[0] for i in edges[:]]

	nodes = [{'name': str(i) } for i in list(set(node_list)) ]
	links = [{'source': u[0], 'target': u[1]} for u in edges ]
	with open(FILENAME, 'w') as f:
		json.dump({'nodes': nodes, 'links': links}, f, indent=4,)
	return


NODE = 'NAT2'
idoptions = 'tissues'

# Run query
# Get list of all the ids for that node

listof_nodes= {each.id: each.name for each in Node.query.filter(Node.name == NODE).all()}
# For each id, get list of all networks associated with it.
listof_networks={}
for key in tqdm(listof_nodes.keys()):
	for one in Network.query.filter(and_(Network.nodes_.any(id=key), Network.context==idoptions)).all():
		listof_networks.update({one.name: [one.data, one.context_info]})

NETWORKS = [graphs[0] for graphs in listof_networks.values()]

for network in tqdm(NETWORKS):
	create_json_file(g=network, node=NODE)

# TODO link this code to the results page, so that every network generates a json file
# TODO add API for a json file for graphs (graph.js should get json from there)


# descargar