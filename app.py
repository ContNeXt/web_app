from flask import Flask, redirect, url_for, render_template, request, session, flash
# from datetime import timedelta

app = Flask(__name__)
app.secret_key = "changethislater"
# app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/page")
def page():
   return render_template("page.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash(f"You have logged in successfully, {user}", "info")

        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        flash(f"You have been logged out, {user}", "info")
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
   return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)


