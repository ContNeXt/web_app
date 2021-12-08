# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
# TODO flask_cors requirements

from homepage import homepage
from models import Network, Node
from querypage import querypage
from autocomplete import query_db_for_nodes
from graph import create_json_file

app = Flask(__name__)

# Initialize the database
db = SQLAlchemy(app)

# SQLAlchemy
db_name = "database.db"

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Add Admin view
admin = Admin(app)
admin.add_view(ModelView(Network, db.session))
admin.add_view(ModelView(Node, db.session))

'''
    URL Builders for website
'''

app.register_blueprint(homepage, url_prefix="")
app.register_blueprint(querypage, url_prefix="")

# app.register_blueprint(models)


@app.route("/")
def main():
	return redirect("home")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/terms")
def terms():
	return render_template("terms.html")


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
	return render_template("explorer.html", network_id=network_id, node=node, network=network)


# autocomplete API: node list json
@app.route("/api/autocomplete", methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def node_autocompletion():
	q = request.form['q']
	print ('term ', q)
	if not q:
		return jsonify({})
	results = query_db_for_nodes(query=q, context='tissues')
	# TODO add context as second query parameter context as second query!!
	print(results)
	return jsonify(results)

# autocomplete API: result json
@app.route("/api/neighbouringnodes/<node>/<network_id>", methods = ['GET'])
def network_explorer(node, network_id):
	if (request.method == 'GET'):
		print(network_id)
		nodes, links = 	create_json_file(id=network_id, node=node)
		return jsonify({'nodes': nodes, 'links': links})


'''
    Run app
'''
if __name__ == "__main__":
	app.run(debug=True)
