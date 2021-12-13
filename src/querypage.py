from flask import Blueprint, render_template, request, redirect, url_for, session
from tqdm import tqdm

from sqlalchemy import and_
from models import Network, Node, relationship_table


querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query")
def query():
    # Import query parameters
    idquery=session.get('query', None)
    idoptions=session.get('idoptions', None)

    # Run query
    # Get list of all the ids for that node
    listof_nodes={each.id : each.name for each in Node.query.filter(Node.name == idquery).all()}

    # For each id, get list of all networks associated with it.
    listof_networks={}
    for node in tqdm(listof_nodes.keys()):
        for network in Network.query.filter(and_(Network.nodes_.any(id=node), Network.context==idoptions)).all():
            listof_networks.update({network.name: [network.data, network.context_info]})

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=listof_networks)
