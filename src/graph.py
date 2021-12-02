import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from sqlalchemy import and_
from models import Network, Node, relationship_table

def create_json_file(g, file):
	fig, ax = plt.subplots(1, 1, figsize=(8, 6))
	nx.draw(g, ax=ax)

	nodes = [{'name': str(i) } for i in g.nodes()]
	links = [{'source': u[0], 'target': u[1]} for u in g.edges()]
	with open(file, 'w') as f:
		json.dump({'nodes': nodes, 'links': links}, f, indent=4,)
	print("Done!")
	return

idquery = 'NAT2'
idoptions = 'tissues'

# Run query
# Get list of all the ids for that node

listof_nodes= { each.id: each.name for each in Node.query.filter(Node.name == idquery).all()}
# For each id, get list of all networks associated with it.
listof_networks={}
for key in tqdm(listof_nodes.keys()):
	for one in Network.query.filter(and_(Network.nodes_.any(id=key), Network.context==idoptions)).all():
		listof_networks.update({one.name: [one.data, one.context_info]})

EDGES = [ graphs[0] for graphs in listof_networks.values() ]
FILENAMES = [ str(each)+'.json' for each in listof_networks.keys() ]

for file, edge in zip(FILENAMES,EDGES):
	create_json_file(g=edge, file=file)

# TODO link this code to the results page, so that every network generates a json file
# TODO add API for a json file for graphs (graph.js should get json from there)


