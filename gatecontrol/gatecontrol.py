'''
Created on 08/nov/2014

@author: spax
'''

STATE_CLOSED = {'id' : 0, 'description' : 'closed'}
STATE_OPEN = {'id' : 1, 'description' : 'open'}


class Gate:
    
    def __init__(self):
        self.state = STATE_CLOSED
    
    def open_gate(self, request=None):
        if request is not None:
            self.state = STATE_OPEN
            request.done()
    
    def get_state(self, request=None):
        return self.state
    
    def is_open(self):
        return self.get_state() == STATE_OPEN
    
    def get_available_states(self):
        return (STATE_OPEN, STATE_CLOSED)
    
