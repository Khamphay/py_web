from flask import Flask, render_template, request
from flask_compress import Compress

app = Flask(__name__, static_folder="static")
Compress(app)

@app.route("/")
def hello():
    data = "Coopsoil Lab"
    return render_template("index.html", data=data)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/data", methods=["POST"])
def data():
    data = request.form
    return render_template("data.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
