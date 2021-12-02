import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from sqlalchemy import and_
from models import Network, Node, relationship_table

idquery = 'NAT2'
idoptions = 'tissues'

# Run query
# Get list of all the ids for that node
listof_nodes_id=[each.id for each in Node.query.filter(Node.name == idquery).all()]

# For each id, get list of all networks associated with it.
listof_networks={}
for each in tqdm(listof_nodes_id[:2]):
	print(each)
	for one in Network.query.filter(and_(Network.nodes_.any(id=each), Network.context==idoptions)).all():
		listof_networks.update({one.name: [one.data, one.context_info]})


for each in tqdm(listof_networks.values()):
	print(each[0].number_of_edges())
	# g = each[0]
	# fig, ax = plt.subplots(1, 1, figsize=(8, 6))
	# nx.draw(g, ax=ax)
	# plt.savefig("/Users/sara/Desktop/filename.png")