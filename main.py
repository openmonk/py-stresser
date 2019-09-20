from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        if len(rule.defaults or []) >= len(rule.arguments or []):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    from pprint import pformat
    return pformat(links)

@app.route("/hc")
def healthcheck():
    return "ok"

@app.route("/skiller")
def skiller():
	return "killed"

if __name__ == "__main__":
    app.run()
