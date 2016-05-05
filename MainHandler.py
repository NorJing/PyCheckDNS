import tornado.ioloop
import tornado.web
import socket
from termcolor import colored

global urls
urls = []
global dtc_ips
dtc_ips = []
global hdc_ips
hdc_ips = []
global DATACENTRES
DATACENTRES = {}

def read_source():
    with open('source', 'r') as f:
        for line in f:
            list = line.split(',')
            urls.append(list[0])
            dtc_ips.append(list[1])
            hdc_ips.append(list[2].rstrip('\n'))

def check_dns(hostname, i):
    dtc_ip = dtc_ips[i]
    hdc_ip = hdc_ips[i]
    ip = socket.gethostbyname(hostname)
    if ip == dtc_ip:
        print ip + colored(' DTC', 'green')
        return "DTC"
    elif ip == hdc_ip:
        print ip + colored(' HDC', 'red')
        return "HDC"
    else:
        return "ERROR"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        DATACENTRES = {}
        i = 0
        for url in urls:
            DATACENTRE = check_dns(url, i)
            i=i+1
            DATACENTRES[url] = DATACENTRE

        self.render("main.html", title="Check DNS", items=DATACENTRES)

def make_app():
    return tornado.web.Application([
        (r"/checkdns", MainHandler),
    ])

if __name__ == "__main__":
    read_source()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
