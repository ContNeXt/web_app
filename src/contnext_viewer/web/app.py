# -*- coding: utf-8 -*-

"""This module contains the ContNeXt Flask Application application."""

import logging
import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from contnext_viewer.web.homepage import homepage
from contnext_viewer.web.querypage import querypage
from contnext_viewer.models import Network, Node, DB_PATH
from contnext_viewer.web.views import contnext

log = logging.getLogger(__name__)


def create_app(template_folder: str = None, static_folder: str = None):
	"""Create the Flask application"""
	t = time.time()

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
		Blueprints for the website
	'''
	app.register_blueprint(contnext)
	app.register_blueprint(querypage, url_prefix="")
	app.register_blueprint(homepage, url_prefix="")

	log.info('Done building %s in %.2f seconds', app, time.time() - t)
	return app


'''
    Run app
'''
if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, host='0.0.0.0', port=5000)
