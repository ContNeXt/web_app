from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Networks, Nodes

querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query")
def query():
    # Import query parameters
    idquery=session.get('query', None)
    idoptions=session.get('idoptions', None)

    # Import dictionary from database

    # Run query
    if idoptions == 'TISS':
        NQuery = Nodes.query.filter(Nodes.name == idquery).all()
        NAnswer=[]
        for each in NQuery:
            answer=Nodes.query.filter(Nodes.which_networks.any(id=each.id)).all()
            NAnswer.append(answer)
        idoptions = "Tissues"

    elif idoptions == 'CELL':
        NQuery = Nodes.query.filter(
            (Nodes.name == idquery)
        ).all()
        idoptions = "Cell Lines"

    elif idoptions == 'CELT':
        NQuery = Nodes.query.filter(
            (Nodes.name == idquery)
        ).all()
        idoptions = "Cell Types"

    elif idoptions == 'SPEC':
        NQuery = Nodes.query.filter(
            (Nodes.name == idquery)
        ).all()
        idoptions = "Species"

    else:
        NQuery = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=NAnswer)
