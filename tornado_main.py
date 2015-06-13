'''
Created on 09/giu/2015

@author: spax
'''

import django.core.handlers.wsgi
from django.conf import settings
from tornado import websocket
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import os
import gatecontrol.notification as notification



django.setup()




def main():
    map(lambda g : g.install(), getattr(settings, 'GATES').values())
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler()
    )
    tornado_app = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
        (r"/socket", notification.ClientSocket),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    ], debug=settings.DEBUG)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8000)
    loop = tornado.ioloop.IOLoop.instance()
    sched = tornado.ioloop.PeriodicCallback(notification.StateMonitor().notify_changes, 1000, io_loop = loop)
    sched.start()
    loop.start()

if __name__ == '__main__':
    main()
