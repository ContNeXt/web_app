# -*- coding: utf-8 -*-

"""This module contains the ContNeXt Flask Application application."""

from flask import Flask, render_template, request, redirect, jsonify, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

import logging

from .homepage import homepage
from .models import Network, Node, DB_PATH
from .querypage import querypage
from .autocomplete import query_db_for_nodes
from .graph import create_json_file

log = logging.getLogger(__name__)

def create_app(template_folder:str=None, static_folder:str=None):
	"""Create the Flask application"""

	app = Flask(__name__,
				template_folder=(template_folder or './templates'),
				static_folder=(static_folder or './static')
				)

	cors = CORS(app, resources={r"/foo": {"origins": "*"}})
	app.config['CORS_HEADERS'] = 'Content-Type'

	app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# Initialize the database
	db = SQLAlchemy(app)

	# Add Admin view
	admin = Admin(app)
	admin.add_view(ModelView(Network, db.session))
	admin.add_view(ModelView(Node, db.session))

	'''
		URL Builders for website
	'''

	app.register_blueprint(homepage, url_prefix="")
	app.register_blueprint(querypage, url_prefix="")

	return app

app = create_app()

@app.route("/")
def main():
	return redirect("home")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/imprint")
def imprint():
	return render_template("imprint.html")


@app.route("/tutorial")
def tutorial():
	return render_template("tutorial.html")


@app.route("/admin")
def admin():
	return render_template("admin.html")

@app.route("/graph/<node>/<network_id>")
def graph(node, network_id):
	nodes, links = create_json_file(id=network_id, node=node)
	network = {'nodes': nodes, 'links': links}
	return render_template("explorer.html", network_id=network_id, node=node, network_json=network)


# autocomplete API: node list json
@app.route("/api/autocomplete", methods = ['POST'])
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
@app.route("/api/neighbouring-nodes/<node>/<network_id>", methods = ['GET'])
def network_explorer(node, network_id):
	if (request.method == 'GET'):
		nodes, links = 	create_json_file(id=network_id, node=node)
		return jsonify({'nodes': nodes, 'links': links})


'''
    Run app
'''
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
