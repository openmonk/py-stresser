from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "apps index here"

if __name__ == "__main__":
    app.run()
