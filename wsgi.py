from flask import Flask

application = Flask(__name__)

@application.route("/")
def index():
    return "apps index here"

@application.route("/hc")
def healthcheck():
    return "ok"

if __name__ == "__main__":
    application.run()
