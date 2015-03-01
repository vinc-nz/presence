'''
Created on 08/nov/2014

@author: spax
'''

import sys

from gatecontrol.gatecontrol import Gate, STATE_CLOSED, STATE_OPEN
import presence
from presence.atlantis import AtlantisModemController, check_modem


STATE_RING = {'value' : 2, 'description' : 'ring'}

class HpccExternal(Gate):
    
    def __init__(self, test_env=False):
        self.test_env = test_env
        if not test_env:
            check_modem()
        
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
        if not test_env:
            try:
                from presence.tilt import rpi_gpio_check
                self.rpi_gpio_check = rpi_gpio_check
            except Exception as e:
                if not test_env:
                    print 'ERROR: could not setup %s: %s' % (HpccInternal.__name__, str(e))
                    sys.exit(1)
    
    def get_state(self, request=None):
        if not self.test_env and self.rpi_gpio_check():
            return STATE_OPEN
        else:
            return STATE_CLOSED
