from flask import Flask, url_for, request, Response
from pprint import pformat
import time
import os
import socket

SLEEP_TIME = 1

app = Flask(__name__)

@app.route("/")
def index():
    rules = []
    for rule in app.url_map.iter_rules():
        rules.append((rule.endpoint, rule.methods, str(rule)))
    return "time = %s\nsleep_time = %d\nhelp = %s\n" % (time.ctime(), SLEEP_TIME, pformat(rules))

@app.route("/hc")
def health_check():
    return "%s: ok\n" % ( time.ctime(), )

@app.route("/socket.eater/<int:nr>")
def socket_eater(nr = 0):
    def omnomnom():
        yield "start eating %d sockets\n" % (nr, )
        scks = []
        for i in range(0,int(nr)):
            scks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            scks[-1].listen(0)
            yield "listenning carefully on %s\n" % ( pformat(scks[-1]), )
        yield "sleeping (onlisten)\n"
        time.sleep(SLEEP_TIME)
        for i in range(0,int(nr)):
            scks[i].close()
            yield "socket closed: %s\n" % ( pformat(scks[i]), )
        yield "socket eater exit\n"
    if int(nr):
        return Response(omnomnom(), mimetype="text/plain")
    else:
    	return "socket eater\n"

@app.route("/fd.eater/<int:nr>")
def fd_eater(nr = 0):
    def omnomnom():
        fds = []
        for n in range(0, int(nr)):
            fds.append(open("spamfile." + str(n), "w"))
            yield "created %s \n" % (pformat(fds[-1]),)
        yield "sleeping (oncreate)\n"
        time.sleep(SLEEP_TIME)
        for n in range(0, int(nr)):
            yield "write %s\n" % (pformat(fds[n]),)
            fds[n].write('stuff')
        yield "sleeping (onclose)\n"
        time.sleep(SLEEP_TIME)
        for n in range(0, int(nr)):
            yield "close %s\n" % (pformat(fds[n]),)
            fds[n].close()
        yield "sleeping (onremove)\n"
        time.sleep(SLEEP_TIME)
        for n in range(0, int(nr)):
            fn = "spamfile." + str(n)
            yield "delete %s\n" % (fn, )
            os.remove(fn)
        yield "file descriptor eater exit\n"
    if int(nr):
        return Response(omnomnom(), mimetype="text/plain")
    else:
        return "file descriptor eater\n"

if __name__ == "__main__":
    app.run()
