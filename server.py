#!/usr/bin/env python

# Redirect by Nginx
#
# /etc/nginx/default.d/feeder.conf
#   location /feeder/files/ {
#       proxy_pass http://127.0.0.1:9999/;
#       proxy_connect_timeout 300;
#       proxy_send_timeout 300;
#       proxy_read_timeout 300;
#       send_timeout 300;
#   }

import os, errno
from signal import signal, SIGINT
import urllib, json
import SimpleHTTPServer
import SocketServer
import socket
import threading
from termcolor import colored
from pprint import pprint 
import daemon
import time


script_path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(script_path+'/files'):
    os.makedirs(script_path+'/files')
if not os.path.exists(script_path+'/files'):
    os.makedirs(script_path+'/files')



def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        return thread
    return wrapper

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    Http.stop()
    exit(0)

class HttpServer(object):
    def __init__(self, port=9999, **kwargs):
        self.port = int(kwargs['port_http'])
        self.path = script_path+'/files'
        self.my_ip = "127.0.0.1"

    @threaded
    def start(self):
        os.chdir(self.path)
        server_address = (self.my_ip, self.port)
        try:
            self.httpd = SocketServer.TCPServer(server_address, SimpleHTTPServer.SimpleHTTPRequestHandler)
            self.httpd.socket.getsockname()
            print (colored('[OK]       ', 'green') + "HTTP server started " )
            self.httpd.serve_forever()
        except OSError:
            print (colored('[Warning]  ', 'red') + 'HTTP '+str(self.my_ip)+':'+str(self.port)+' port in use')
            exit(1)

    def stop(self):
        print(colored('[OK]       ', 'yellow') + "HTTP stopping..")
        self.httpd.shutdown()
        return

def print_work_a():
    print('Starting of thread :', threading.currentThread().name)
    time.sleep(211)
    print('Finishing of thread :', threading.currentThread().name)

def write_pidfile_or_die(path_to_pidfile):
    pid = 0
    if os.path.exists(path_to_pidfile):
        pid = int(open(path_to_pidfile).read())

    if pid_is_running(pid):
        print("Process {0} is still running.".format(pid))
        raise SystemExit
    else:
        if os.path.exists(path_to_pidfile):
            os.remove(path_to_pidfile)

    open(path_to_pidfile, 'w').write(str(os.getpid()))
    return path_to_pidfile

def pid_is_running(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return
    else:
        return pid


# Collect Facts
if __name__ == "__main__":
    write_pidfile_or_die('/var/run/python_www_server.pid')
    signal(SIGINT, handler) 
    kwargs = dict()
    print(colored('[facts]    ', 'blue') + "Start hosting WWW Server on " + colored("127.0.0.1:9999", 'green') )


    # HTTP
    kwargs['port_http'] = "9999"
    Http = HttpServer(**kwargs)
    handle_http_t = Http.start()
    

    time.sleep(3600)









