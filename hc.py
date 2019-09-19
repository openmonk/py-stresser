from flask import Flask

app = Flask(__name__)

@app.route("/hc")
def hello():
    return "ok"
