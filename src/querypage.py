from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from load_db import Networks, Nodes

querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query")
def query():
    # Import query parameters
    idquery=session.get('query', None)
    idoptions=session.get('idoptions', None)

    # Run query
    if idoptions == 'NET':
        NQuery = Networks.query.filter(
        (Networks.geneStart == idquery) | (Networks.geneEnd == idquery)
        ).all()
        idoptions = "Networks Database"
    elif idoptions == 'NOD':
        NQuery = Nodes.query.filter(
            (Nodes.name == idquery)
        ).all()
        idoptions = "Nodes Database"
    else:
        NQuery = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=NQuery)
