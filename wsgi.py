from flask import Flask, url_for

application = Flask(__name__)

@application.route("/")
def index():
    links = []
    for rule in application.url_map.iter_rules():
        if len(rule.defaults or []) >= len(rule.arguments or []):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return str(links)

@application.route("/hc")
def healthcheck():
    return "ok"

if __name__ == "__main__":
    application.run()
