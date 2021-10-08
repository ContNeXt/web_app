from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = "changethislater"

@app.route("/")
def home():
   return render_template("home.html")

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

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email =request.form["email"]
            session["email"] = email
            flash(f"Your email is saved: {email}.", "info")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)

    else:
        flash("You are not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        session.pop("email", None)
        flash(f"You have been logged out, {user}", "info")
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
   return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)



