from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from load_db import Network, Node

homepage = Blueprint("homepage", __name__, static_folder="static", template_folder="templates")

@homepage.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Fetch query data
        # Turn into all caps to avoid error
        session['query'] = request.form['query'].upper()
        session['idoptions'] = request.form['queryOptions']

        return redirect(url_for("querypage.query"))
    else:
        return render_template("home.html")

