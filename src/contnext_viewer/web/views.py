# -*- coding: utf-8 -*-
"""This module contains the ContNeXt views."""

import logging
import re


from flask import jsonify, Blueprint, render_template, request, redirect, url_for, session
from flask_cors import cross_origin
from pkg_resources import resource_filename
from sqlalchemy.orm import sessionmaker, scoped_session

from contnext_viewer.constants import CONTEXT
from contnext_viewer.graph import create_json_file
from contnext_viewer.models import Network, Node, engine
from contnext_viewer.web.autocomplete import autocomplete_search

log = logging.getLogger(__name__)

contnext = Blueprint(
    'contnext_viewer',
    __name__,
    template_folder=resource_filename('contnext_viewer', 'templates'),
    static_folder=resource_filename('contnext_viewer', 'templates')
)

sqlsession = scoped_session(sessionmaker(bind=engine))


@contnext.teardown_request
def remove_session(ex=None):
    sqlsession.remove()


@contnext.route("/")
def main():
    """Redirect to ContNeXt home page."""
    return redirect(url_for("contnext_viewer.home"))


@contnext.route("/home", methods=['GET', 'POST'])
def home():
    """Search function in Home"""
    if request.method == 'POST':
        try:
            if request.form.get('node-query') and request.form.get('queryOptions'):
                # Fetch query data
                session['node-query'] = request.form['node-query']
                session['idoptions'] = request.form['queryOptions']
                session['form'] = 'node'
                return redirect(url_for("contnext_viewer.query", query=session['node-query']))

            elif request.form.get('network-query'):
                # Fetch query data
                session['network-query'] = request.form['network-query']
                session['form'] = 'network'
                # check if query is an id or a network name
                if re.match('(UBERON|CL|CLO):\d+', session['network-query']):
                    session['query-param'] = 'identifier'
                else:
                    session['query-param'] = 'name'
                return redirect(url_for("contnext_viewer.query", query=session['network-query']))
        except:
            return render_template("error500.html")
    else:
        return render_template("home.html")


@contnext.route("/query/<query>")
def query(query):
    """Generate results according to query"""
    # Import query parameters
    context = session.get('idoptions', None)
    param = session.get('query-param', None)
    form = session.get('form', None)

    # Start database session
    try:
        if form == 'node':
            # Get list of all the ids for that node
            node_ids = [each.id for each in sqlsession.query(Node).filter(Node.name == query).all()]

            # For each id, get list of all networks associated with it.
            list_of_nodes = {}
            qry = sqlsession.query(Node).filter(Node.id == node_ids[0])
            for node in qry.all():

                for network in node.networks_:
                    if network.context != context:
                        continue

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
    except IndexError:
        return render_template("error500.html")


@contnext.route("/heatmap/<context>")
def heatmap(context):
    if CONTEXT.get(context):
        title = CONTEXT.get(context)
        if context == 'cell_line' or context == 'cellline':
            json_path = "/static/json/cellline-pathway_clustergrammer.json"
        elif context == 'cell_type' or context == 'celltype':
            json_path = "/static/json/celltype-pathway_clustergrammer.json"
        elif context == 'tissue' or context == 'tissue':
            json_path = "/static/json/tissue-pathway_clustergrammer.json"
        return render_template("heatmaps.html", title=title, json_path=json_path)
    else:
        return render_template("error404.html")


@contnext.route("/about")
def about():
    return render_template("about.html")


@contnext.route("/imprint")
def imprint():
    return render_template("imprint.html")


@contnext.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


@contnext.route("/admin")
def admin():
    return render_template("admin.html")


@contnext.route("/graph/<node>/<network_id>")
def graph(node, network_id):
    nodes, links = create_json_file(id=network_id, node=node)
    network = {'nodes': nodes, 'links': links}
    return render_template("explorer.html", network_id=network_id, node=node, network_json=network)


# autocomplete API: node list json
@contnext.route("/api/autocomplete", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'], support_credentials=True)
def node_autocompletion():
    q = request.form['q']
    resource = request.form['resource']
    if not q or not resource:
        return jsonify({})

    results = autocomplete_search(query=q, context=resource, limit=10)
    if not results:
        return jsonify({})

    return jsonify(results)


# network explorer API: result json
@contnext.route("/api/neighbouring-nodes/<node>/<network_id>", methods=['GET'])
def network_explorer(node, network_id):
    if (request.method == 'GET'):
        nodes, links = create_json_file(id=network_id, node=node)
        return jsonify({'nodes': nodes, 'links': links})


# Error handling
@contnext.errorhandler(404)
def not_found():
    return render_template("error404.html")


@contnext.errorhandler(500)
def not_found():
    return render_template("error404.html")
