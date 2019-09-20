from flask import Flask, url_for, request, Response
from pprint import pformat
import time
import os

app = Flask(__name__)

@app.route("/")
def index():
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))
    return pformat(rules) + "\n"

@app.route("/hc")
def healthcheck():
    return "ok\n"

@app.route("/skiller")
def skiller():
	return "todo:socket killer\n"

@app.route("/fdkill/<nr>")
def fdkill(nr=1):
    def mkfd():
        fds = []
        for n in range(0, int(nr)):
            fds.append(open("spamfile." + str(n), "w"))
            yield "created %s \n" % (pformat(fds[-1]),)
        yield "sleeping (oncreate)\n"
        time.sleep(60)
        for n in range(0, int(nr)):
            yield "write %s\n" % (pformat(fds[n]),)
            fds[n].write('stuff')
        yield "sleeping (onclose)\n"
        time.sleep(60)
        for n in range(0, int(nr)):
            yield "close %s\n" % (pformat(fds[n]),)
            fds[n].close()
        yield "sleeping (onremove)\n"
        time.sleep(60)
        for n in range(0, int(nr)):
            fn = "spamfile." + str(n)
            yield "delete %s\n" % (fn, )
            os.remove(fn)
        yield "stress done\n"

    return Response(mkfd(), mimetype="text/plain")

if __name__ == "__main__":
    app.run()
