# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from .models import Network, Node, engine


querypage = Blueprint("querypage", __name__, static_folder="static", template_folder="templates")

@querypage.route("/query/<query>")
def query(query):

    # Import query parameters
    context = session.get('idoptions', None)
    param = session.get('query-param', None)
    form = session.get('form', None)

    # Start database session
    Session = sessionmaker(bind=engine)
    sqlsession = Session()

    if form == 'node':
        # Get list of all the ids for that node
        node_id = [ each.id for each in sqlsession.query(Node).filter(Node.name == query).all()]
        # For each id, get list of all networks associated with it.
        list_of_nodes = {}
        for network in sqlsession.query(Network).filter(and_(Network.nodes_.any(id=node_id[0]), Network.context == context)).all():
            list_of_nodes.update({network.identifier: [network.data, network.name, network.properties]})
        return render_template("results.html", idquery=query, idoptions=context, form=form, results=list_of_nodes)


    elif form == 'network' and param == 'identifier':
        # Get network info
        list_of_networks = [[network.identifier, network.data, network.name, network.properties, network.context]
                           for network in sqlsession.query(Network).filter(Network.identifier == query).all()][0]
        return render_template("results.html", idquery=query, idoptions=context, form=form,
                               results=list_of_networks)


    elif form == 'network' and param == 'name':
        # Get network info
        list_of_networks = [[network.identifier, network.data, network.name, network.properties, network.context]
                           for network in sqlsession.query(Network).filter(Network.name == query).all()][0]
        return render_template("results.html", idquery=query, idoptions=context, form=form,
                               results=list_of_networks)

