from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Network, Node

querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query")
def query():
    # Import query parameters
    idquery=session.get('query', None)
    idoptions=session.get('idoptions', None)

    # Import dictionary from database

    # Run query
    if idoptions == 'TISS':
        NQuery = Node.query.filter(Node.name == idquery).all()
        NAnswer=[]
        for each in NQuery:
            answer=Node.query.filter(Node.network.any(id=each.id)).all()
            NAnswer.append(answer)
        idoptions = "Tissues"

    elif idoptions == 'CELL':
        NQuery = Node.query.filter(
            (Node.name == idquery)
        ).all()
        idoptions = "Cell Lines"

    elif idoptions == 'CELT':
        NQuery = Node.query.filter(
            (Node.name == idquery)
        ).all()
        idoptions = "Cell Types"

    elif idoptions == 'SPEC':
        NQuery = Node.query.filter(
            (Node.name == idquery)
        ).all()
        idoptions = "Species"

    else:
        NQuery = "Something went wrong"

    return render_template("results.html", idquery=idquery, idoptions=idoptions, results=NAnswer)
