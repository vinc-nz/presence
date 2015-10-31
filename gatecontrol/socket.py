'''
Created on 10/giu/2015

@author: spax
'''

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
        self.api = ApiView()
        
    def on_message(self, message):
        try:
            method = getattr(self.api, message['method'])
            return method(message['args'])
        except Exception:
            pass
        
    def push_info(self):
        self.write_message(self.api.list_gates())

    def on_close(self):
        StateMonitor.clients.remove(self)
