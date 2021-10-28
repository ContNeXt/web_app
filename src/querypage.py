from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Network, Node
from pickler import unpickle_network

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
        NAnswer=[]
        for each in listof_nodes_id:
            answer = [unpickle_network(each.data) for each in Network.query.filter(Network._nodes.any(id=each)).all()]
            NAnswer.append(answer)

        idoptions = "Tissues"

    else:
        NQuery = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=NAnswer)
