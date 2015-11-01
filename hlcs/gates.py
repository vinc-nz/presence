'''
Created on 08/nov/2014

@author: spax
'''

import re
import sys
import traceback

from django.conf import settings

from gatecontrol.models import GateController, GATE_STATE_OPEN, \
    GATE_STATE_CLOSED
from hlcs.modem import AtlantisModem


GATE_STATE_RING = 'ring'
GATE_STATE_UNKNOWN =  'unknown'

def setup():
    try:
        HpccExternal.setup()
        HpccInternal.setup()
    except Exception as e:
        traceback.print_exc()
        exit(1)

class HpccExternal(GateController):
    
    state = GATE_STATE_UNKNOWN
    
    @classmethod
    def setup(cls):
        AtlantisModem().check_connection()

    def __init__(self, modem=None):
        self.modem = AtlantisModem()
            
    def get_state(self):
        return HpccExternal.state

    def handle_request(self, access_request):
        self.controller = self.modem.get_controller()
        self.controller.setup(access_request, self.reset_state)
        HpccExternal.state = GATE_STATE_RING
        
    def reset_state(self):
        HpccExternal.state = GATE_STATE_UNKNOWN
        
    def is_managed_by_user(self, user):
        if not user:
            return False
        if HpccExternal.state == GATE_STATE_RING:
            return False
        return True




class HpccInternal(GateController):


    @classmethod
    def setup(cls):
        from hlcs.gpio import setup, magnet_input, send_open_pulse
        setup()
        cls.magnet_input = magnet_input
        cls.send_open_pulse = send_open_pulse

    def get_state(self):
        is_open = HpccInternal.magnet_input()
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
        HpccInternal.send_open_pulse()
        access_request.done()
           
