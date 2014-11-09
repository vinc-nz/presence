'''
Created on 08/nov/2014

@author: spax
'''

STATE_CLOSED = {'value' : 0, 'description' : 'closed'}
STATE_OPEN = {'value' : 1, 'description' : 'open'}


class Gate:
    
    def open_gate(self, request):
        pass
    
    def get_state(self, request=None):
        return STATE_CLOSED
    
    def get_available_states(self):
        return (STATE_OPEN, STATE_CLOSED)
    
    def get_busy_state(self):
        return STATE_CLOSED