'''
Created on 08/nov/2014

@author: spax
'''

from gatecontrol.gatecontrol import Gate, STATE_CLOSED, STATE_OPEN
from presence.atlantis import AtlantisModemController
from presence.tilt import rpi_gpio_check


STATE_RING = {'value' : 2, 'description' : 'ring'}

class HpccExternal(Gate):
    
    def __init__(self, test_env=False):
        self.test_env = test_env
        
    def get_available_states(self):
        return (STATE_CLOSED, STATE_OPEN, STATE_RING)
    
    def open_gate(self, request):
        self.controller = AtlantisModemController(test_env=self.test_env)
        self.controller.setup(request)
        self.controller.start()
        
    def get_state(self, request=None):
        if request is None:
            return STATE_CLOSED
        elif request.is_ok():
            return STATE_OPEN
        elif request.is_pending():
            return STATE_RING
        else:
            return STATE_CLOSED
    
    def get_busy_state(self):
        return STATE_RING
        
        
class HpccInternal(Gate):
    
    def __init__(self, test_env=False):
        self.test_env = test_env
    
    def get_state(self, request=None):
        if not self.test_env and rpi_gpio_check():
            return STATE_OPEN
        else:
            return STATE_CLOSED
