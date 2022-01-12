# -*- coding: utf-8 -*-

"""This module contains the ContNeXt views."""

import logging

from flask import jsonify, Blueprint
from flask import render_template, request
from flask_cors import cross_origin
from pkg_resources import resource_filename

from autocomplete import query_db_for_nodes
from contnext_viewer.graph import create_json_file

log = logging.getLogger(__name__)

contnext = Blueprint(
	'contnext_viewer',
	__name__,
	template_folder=resource_filename('contnext_viewer', 'templates'),
	static_folder=resource_filename('contnext_viewer', 'static')
)


@contnext.route("/")
def main():
	"""Redirect to ContNeXt home page."""
	return render_template("home.html")


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
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def node_autocompletion():
	q = request.form['q']
	resource = request.form['resource']
	if not q or not resource:
		return jsonify({})

	results = query_db_for_nodes(query=q, context=resource, limit=10)
	if not results:
		return jsonify({})

	return jsonify(results)


# autocomplete API: result json
@contnext.route("/api/neighbouring-nodes/<node>/<network_id>", methods=['GET'])
def network_explorer(node, network_id):
	if (request.method == 'GET'):
		nodes, links = create_json_file(id=network_id, node=node)
		return jsonify({'nodes': nodes, 'links': links})
