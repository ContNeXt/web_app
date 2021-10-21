from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from homepage import homepage
from querypage import querypage

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

app.register_blueprint(homepage, url_prefix="")
app.register_blueprint(querypage, url_prefix="")


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


'''
    Run app
'''
if __name__ == "__main__":
    app.run(debug=True)

