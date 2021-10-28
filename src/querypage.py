from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Network, Node
from pickler import unpickle_network
from collections import namedtuple
import networkx as nx
from tqdm import tqdm


querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query")
def query():
    # Import query parameters
    idquery=session.get('query', None)
    idoptions=session.get('idoptions', None)

    # Import dictionary from database

    # Run query
    if idoptions == 'TISS':
        # Get list of all the ids for that node
        listof_nodes_id=[each.id for each in Node.query.filter(Node.name == idquery).all()]

        # For each id, get list of all networks associated with it.
        listof_networks=[]
        for each in tqdm(listof_nodes_id):
            for one in Network.query.filter(Network._nodes.any(id=each)).all():
                a_network = unpickle_network(one.data)
                a_network_as_list = [nx.edges(a_network),
                                     nx.get_edge_attributes(a_network, 'direction'),
                                     nx.get_edge_attributes(a_network, 'method'),
                                     nx.get_edge_attributes(a_network,'weight')
                                     ]
                listof_networks.append(a_network_as_list)

                # Turn result into list

        idoptions = "Tissues"

    else:
        result = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=listof_networks)
