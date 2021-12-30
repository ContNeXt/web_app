from flask import Blueprint, render_template, request, redirect, url_for, session
from tqdm import tqdm

from sqlalchemy import and_
from models import Network, Node, relationship_table


querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query/<query>")
def query(query):
    # Import query parameters
    context = session.get('idoptions', None)
    param = session.get('query-param', None)
    form = session.get('form', None)
    if form == 'node':
        # Run query
        # Get list of all the ids for that node
        listof_nodes={each.id : each.name for each in Node.query.filter(Node.name == query).all()}
        # For each id, get list of all networks associated with it.
        listof_networks={}
        for node in tqdm(listof_nodes.keys()):
            for network in Network.query.filter(and_(Network.nodes_.any(id=node), Network.context == context)).all():
                listof_networks.update({network.identifier: [network.data, network.name, network.properties]})

    elif form == 'network' and param == 'identifier':
        listof_networks = [[network.identifier, network.data, network.name, network.properties, network.context]
                           for network in Network.query.filter(Network.identifier == query).all()][0]

    elif form == 'network' and param == 'name':
        listof_networks = [[network.identifier, network.data, network.name, network.properties, network.context]
                           for network in Network.query.filter(Network.name == query).all()][0]

    return render_template("results.html", idquery=query, idoptions=context, form=form, results=listof_networks)
