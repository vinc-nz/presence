'''
Created on 10/giu/2015

@author: spax
'''

import json
import sys
import traceback

from tornado import websocket

from gatecontrol.models import Gate
from gatecontrol.views import ApiView


class StateMonitor:
    
    clients = []
    
    def push_to_all(self):
        for client in StateMonitor.clients:
            client.push_info()

    def __init__(self):
        self.current = self.read_all_states()
        
    def read_all_states(self):
        return [g.controller().get_state() for g in Gate.objects.all()]


    def notify_changes(self):
        new_states = self.read_all_states()
        if self.current != new_states:
            self.current = new_states
            self.push_to_all()



class ClientSocket(websocket.WebSocketHandler):
    
    def open(self):
        StateMonitor.clients.append(self)
        self.api = ApiView(self.request.remote_ip)
        self.push_info()
        

    def _call_api_method(self, method_name, args={}):
        method = getattr(self.api, method_name)
        try:
            response = method(**args)
            message = {'type':method_name, 'content':response}
            self.write_message(message)
        except Exception as e:
            self.write_message({'type':'error', 'content': e.get_info()})

    def on_message(self, message):
        try:
            if isinstance(message, str):
                message = json.loads(message)
            method_name = message['method']
            args = message['args']
            self._call_api_method(method_name, args)
        except:
            self.write_message({'type':'error', 'content': 'invalid message received'})
        
    def push_info(self):
        self._call_api_method('list_gates')

    def on_close(self):
        StateMonitor.clients.remove(self)
        
    def check_origin(self, origin):
        return True
