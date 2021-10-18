from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# !!!!!!! change this to models when separate file is made
from load_db import Networks, Nodes

# import os
# currentDirectory = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

# SQLAlchemy
db_name = 'testDatabase.db'

app.config['SECRET_KEY'] = "1P313P4OO138O4UQRP9343P4AQEKRFLKEQRAS230"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

'''
    URL Builders for website
'''

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Fetch query data
        query = request.form['query']
        queryOptions = request.form['queryOptions']

        # !!!!!! MAKE SEPARATE
        # Run query
        NETQuery = Networks.query.filter(
            (Networks.geneStart == query) | (Networks.geneEnd == query)
        ).all()

        return redirect(url_for("query", idquery=query))
    else:
        return render_template("home.html")

@app.route("/query/<idquery>")
def query(idquery):
    return render_template("results.html", idquery=idquery)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


'''
    Run app
'''
if __name__ == "__main__":
    app.run(debug=True)

