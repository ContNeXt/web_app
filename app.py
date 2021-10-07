from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return 'Hello! This is the main page <h1>HELLO<h1'

@app.route("/<name>")
def user(name):
    return ƒ'Hello {name}'

if __name__ == '__main__':
    app.run()


