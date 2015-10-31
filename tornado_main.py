'''
Created on 09/giu/2015

@author: spax
'''

import asyncio

from django.conf import settings
import django.core.handlers.wsgi
import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.wsgi

import gatecontrol.socket as socket


django.setup()


def main():
    AsyncIOMainLoop().install()
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler()
    )
    tornado_app = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
        (r"/socket", socket.ClientSocket),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    ], debug=settings.DEBUG)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8000)
    sched = tornado.ioloop.PeriodicCallback(socket.StateMonitor().notify_changes, 1000, io_loop=IOLoop.instance())
    sched.start()
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
