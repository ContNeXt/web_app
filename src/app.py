from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from homepage import homepage
from querypage import querypage

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Network, Node

app = Flask(__name__)


# Initialize the database
db = SQLAlchemy(app)

# SQLAlchemy
db_name = "database.db"

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
#app.register_blueprint(models)


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
'''
    Run app
'''
if __name__ == "__main__":
    app.run(debug=True)

