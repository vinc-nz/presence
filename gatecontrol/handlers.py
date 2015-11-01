'''
Created on 10/giu/2015

@author: spax
'''

import json
import logging

from django.contrib.auth import authenticate
from tornado import websocket
import tornado

from gatecontrol.monitor import StateMonitor
from gatecontrol.views import ApiView


logger = logging.getLogger(__name__)

class TokenHandler(tornado.web.RequestHandler):
    
    def post(self):
        try:
            auth_request = json.loads(self.request.body.decode())
            user = authenticate(username=auth_request['username'], password=auth_request['password'])
            if user is not None:
                self.write({'type': 'token', 'content': ApiView._create_token(user.username).decode()})
            else:
                self.set_status(401)
                self.write({'type': 'error', 'content': "The username and password were incorrect."})
        except Exception as e:
            logger.exception(e)
            self.set_status(400)
            self.write({'type': 'error', 'content': "Bad request"})
            
            


class SocketHandler(websocket.WebSocketHandler):
    
    def open(self):
        StateMonitor.clients.append(self)
        self.api = ApiView(self.request.remote_ip)
        

    def _call_api_method(self, method_name, args={}):
        method = getattr(self.api, method_name)
        try:
            response = method(**args)
            message = {'type':method_name, 'content':response}
            self.write_message(message)
        except Exception as e:
            logger.exception(e)
            self.write_message({'type':'error', 'content': str(e)})

    def on_message(self, message):
        try:
            if isinstance(message, str):
                message = json.loads(message)
            method_name = message['method']
            args = message['args']
            self._call_api_method(method_name, args)
        except Exception as e:
            logger.exception(e)
            self.write_message({'type':'error', 'content': 'invalid message received'})
        
    def push_info(self):
        self._call_api_method('list_gates')

    def on_close(self):
        StateMonitor.clients.remove(self)
        
    def check_origin(self, origin):
        return True
