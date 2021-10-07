from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/page")
def page():
   return render_template("page.html")

@app.route("/admin")
def admin():
   return render_template("admin.html")

#@app.route("/<name>")
#def user(name):
#    return f'Hello {name}!'

#@app.route("/admin")
#def admin():
#    return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run(debug=True)


