from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Network, Node
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
        listof_networks={}
        for each in tqdm(listof_nodes_id):
            for one in Network.query.filter(Network._nodes.any(id=each)).all():
                listof_networks.update({one.name: one.data})
        idoptions = "Tissues"

    else:
        result = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=listof_networks)
