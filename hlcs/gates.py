'''
Created on 08/nov/2014

@author: spax
'''

import sys

from hlcs.modem import AtlantisModem
from django.conf import settings
import re
from gatecontrol.models import GateController, GATE_STATE_OPEN,\
    GATE_STATE_CLOSED


GATE_STATE_RING = 'ring'
GATE_STATE_UNKNOWN =  'unknown'

class HpccExternal(GateController):
    
    state = 'unknown'

    def __init__(self, modem=None):
        self.state = GATE_STATE_UNKNOWN
        if modem is None:
            self.modem = AtlantisModem()
        else:
            self.modem = modem
            
    def get_state(self):
        return HpccExternal.state

    def handle_request(self, access_request):
        if self.is_managed_by_user(access_request.user, access_request.address):
            self.controller = self.modem.get_controller()
            self.controller.setup(access_request, self.reset_state)
            HpccExternal.state = GATE_STATE_RING
        else:
            access_request.fail('Forbidden')
        
    def reset_state(self):
        self.state = GATE_STATE_UNKNOWN
        
    def is_managed_by_user(self, user):
        if not user:
            return False
        if self.state == GATE_STATE_RING:
            return False
        return True




class HpccInternal(GateController):

    def __init__(self):
        pass

    def install(self):
        try:
            from hlcs.gpio import magnet_input, send_open_pulse
            self.magnet_input = magnet_input
            self.send_open_pulse = send_open_pulse
        except Exception as e:
            print ('ERROR: could not setup %s: %s' % (HpccInternal.__name__, str(e)))
            sys.exit(1)

    def get_state(self):
        is_open = self.magnet_input()
        return GATE_STATE_OPEN if is_open else GATE_STATE_CLOSED

    def _ip_is_authorized(self, address):
        pattern = getattr(settings, 'IP_PATTERN', '10.87.1.\d+')
        return re.match(pattern, address)
    
    def is_managed_by_user(self, user, ip_address):
        if not user:
            return False
        if not user.is_staff():
            return False
        if not self._ip_is_authorized(ip_address):
            return False
        return True

    def handle_request(self, access_request):
        if self.is_managed_by_user(access_request.user, access_request.address):
            self.send_open_pulse()
            access_request.done()
        else:
            access_request.fail('Forbidden')
