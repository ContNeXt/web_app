from flask import Blueprint, render_template, request, redirect, url_for, session

homepage = Blueprint("homepage", __name__, static_folder="static", template_folder="templates")

@homepage.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Fetch query data
        session['query'] = request.form['query']
        session['idoptions'] = request.form['queryOptions']

        return redirect(url_for("querypage.query"))
    else:
        return render_template("home.html")
