from flask import Flask, url_for, request, Response
from pprint import pformat
import time
import os
import socket
import threading

app = Flask(__name__)
app.config['STRESS_DELAY'] = 5

@app.route("/")
def index():
    rules = []
    for rule in app.url_map.iter_rules():
        rules.append((rule.endpoint, rule.methods, str(rule)))
    return "time = %s\STRESS_DELAY = %d\nhelp = %s\n" % (time.ctime(), app.config['STRESS_DELAY'], pformat(rules))

@app.route("/hc")
def health_check():
    return "%s: ok\n" % ( time.ctime(), )

@app.route("/stress.delay/<int:seconds>")
def set_stress_delay(seconds = 10):
    app.config['STRESS_DELAY'] = seconds
    return "%s: STRESS_DELAY=%d\n" % ( time.ctime(), app.config['STRESS_DELAY'] )

@app.route("/tread.eater/<int:nr>")
def thread_eater(nr = 0):
    def do_nothing():
        time.sleep(app.config['STRESS_DELAY'])
    def omnomnom():
        yield "start eating %d threads\n" % (nr, )
        threads = list()
        for i in range(nr):
            threads.append(threading.Thread(target=do_nothing, args=()))
            threads[-1].start()
            yield "#%d# thread started: %s\n" % ( i, pformat(threads[-1]) )
        yield "waiting for threads (%d sec or so)\n" % ( app.config['STRESS_DELAY'], )
        for t in threads:
            t.join()
            yield "thread finished: %s\n" % ( pformat(t),  )
        yield "thread eater exit\n"
    if int(nr):
        return Response(omnomnom(), mimetype="text/plain")
    else:
        return "thread eater\n"

@app.route("/socket.eater/<int:nr>")
def socket_eater(nr = 0):
    def omnomnom():
        yield "start eating %d sockets\n" % (nr, )
        scks = []
        for i in range(0,int(nr)):
            scks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            scks[-1].listen(0)
            yield "#%d# listenning carefully on %s\n" % ( i, pformat(scks[-1]) )
        yield "sleeping (onlisten)\n"
        time.sleep(app.config['STRESS_DELAY'])
        for i in range(0,int(nr)):
            scks[i].close()
            yield "#%d# socket closed: %s\n" % ( i, pformat(scks[-1]) )
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
            yield "#%d# created %s \n" % ( n, pformat(fds[-1]) )
        yield "sleeping (oncreate)\n"
        time.sleep(app.config['STRESS_DELAY'])
        for n in range(0, int(nr)):
            yield "#%d# write %s\n" % ( n, pformat(fds[n]) )
            fds[n].write('stuff')
        yield "sleeping (onclose)\n"
        time.sleep(app.config['STRESS_DELAY'])
        for n in range(0, int(nr)):
            yield "#%d# close %s\n" % ( n, pformat(fds[n]) )
            fds[n].close()
        yield "sleeping (onremove)\n"
        time.sleep(app.config['STRESS_DELAY'])
        for n in range(0, int(nr)):
            fn = "spamfile." + str(n)
            yield "#%d# delete %s\n" % ( n, fn )
            os.remove(fn)
        yield "file descriptor eater exit\n"
    if int(nr):
        return Response(omnomnom(), mimetype="text/plain")
    else:
        return "file descriptor eater\n"

if __name__ == "__main__":
    app.run()
