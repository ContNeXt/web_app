# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, session
import re

homepage = Blueprint("homepage", __name__, static_folder="static", template_folder="templates")

@homepage.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('node-query') and request.form.get('queryOptions'):
            # Fetch query data
            session['node-query'] = request.form['node-query']
            session['idoptions'] = request.form['queryOptions']
            session['form'] = 'node'
            return redirect(url_for("querypage.query", query=session['node-query']))

        elif request.form.get('network-query'):
            # Fetch query data
            session['network-query'] = request.form['network-query']
            session['form'] = 'network'
            # check if query is an id or a network name
            if re.match('(UBERON|CL|CLO):\d+', session['network-query']):
                session['query-param'] = 'identifier'
            else:
                session['query-param'] = 'name'
            return redirect(url_for("querypage.query", query=session['network-query']))
    else:
        return render_template("home.html")
