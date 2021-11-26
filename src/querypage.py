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
    listof_nodes_id=[each.id for each in Node.query.filter(Node.name == idquery).all()]

    # For each id, get list of all networks associated with it.
    listof_networks={}
    for each in tqdm(listof_nodes_id):
        for one in Network.query.filter(and_(Network.nodes_.any(id=each), Network.context==idoptions)).all():
            listof_networks.update({one.name: [one.data, one.context]})

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=listof_networks)
