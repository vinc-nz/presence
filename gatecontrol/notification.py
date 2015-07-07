'''
Created on 10/giu/2015

@author: spax
'''

from tornado import websocket
from django.conf import settings
clients = []

gates = getattr(settings, 'GATES', {})

def read_all_states():
    states_dict = {}
    for name, gate in gates.items():
        states_dict[name] = gate.read_state()
    return states_dict


def push_to_all(data):
    for client in clients:
        client.write_message(data)

class StateMonitor:

    def __init__(self):
        self.current = read_all_states()


    def notify_changes(self):
        new_states = read_all_states()
        if self.current != new_states:
            self.current = new_states
            push_to_all(new_states)



class ClientSocket(websocket.WebSocketHandler):
    def open(self):
        clients.append(self)
        self.write_message(read_all_states())

    def on_close(self):
        clients.remove(self)
