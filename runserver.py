'''
Created on 09/giu/2015

@author: spax
'''

import asyncio
import importlib
import os

import django


import django.core.handlers.wsgi
import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.wsgi


from tornado.options import define, options



define("settings", default="presence.settings", help="Django settings module")
define("port", default=8000, help="linsten port")

def setup_gates(settings):
    gate_setup_func = getattr(settings, 'GATE_SETUP_FUNCTION', None)
    if gate_setup_func:
        module_name, function_name = gate_setup_func.rsplit(".", 1)
        the_function = getattr(importlib.import_module(module_name), function_name)
        the_function()

def setup_server(settings):
    import gatecontrol.handlers as handlers
    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application([
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path':'static'}), 
            (r"/socket", handlers.SocketHandler),
            (r"/token", handlers.TokenHandler),  
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))], 
        debug=settings.DEBUG)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, '0.0.0.0')


def setup_periodical_tasks(settings):
    import gatecontrol.monitor as monitor
    callback_time = getattr(settings, 'PERIODIC_CALLBACK_TIME', 100)
    scheduler = tornado.ioloop.PeriodicCallback(monitor.StateMonitor().notify_changes, callback_time, io_loop=IOLoop.instance())
    scheduler.start()

def runserver():
    tornado.options.parse_command_line()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", options.settings)
    django.setup()
    from django.conf import settings
    setup_gates(settings)
    AsyncIOMainLoop().install()
    setup_server(settings)
    setup_periodical_tasks(settings)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    runserver()
