'''
Created on 08/nov/2014

@author: spax
'''

STATE_CLOSED = {'id' : 0, 'description' : 'closed'}
STATE_OPEN = {'id' : 1, 'description' : 'open'}


class Gate:

    def __init__(self):
        self.state = STATE_CLOSED

    def install(self):
        pass
    
    def can_open(self, **kwargs):
        if self.is_open():
            return (False, 'Gate is already open')
        return (True, None)

    def open_gate(self, request):
        if request is None:
            raise Exception('Access Request is None')
        self.state = STATE_OPEN
        request.done()

    def read_state(self):
        return self.state

    def is_open(self):
        return self.read_state() == STATE_OPEN

    def get_available_states(self):
        return (STATE_OPEN, STATE_CLOSED)
