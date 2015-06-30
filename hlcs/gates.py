'''
Created on 08/nov/2014

@author: spax
'''

import sys

from gatecontrol.gatecontrol import Gate, STATE_CLOSED, STATE_OPEN
from hlcs.modem import AtlantisModem
from django.conf import settings
import re


STATE_RING = {'id' : 2, 'description' : 'ring'}
STATE_UNKNOWN = {'id' : 3, 'description' : 'unknown'}

class HpccExternal(Gate):

    def __init__(self, modem=None):
        self.state = STATE_UNKNOWN
        if modem is None:
            self.modem = AtlantisModem()
        else:
            self.modem = modem
            
    def install(self):
        self.modem.check_connection()

    def read_state(self):
        return self.state

    def get_available_states(self):
        return (STATE_UNKNOWN, STATE_RING)

    def open_gate(self, request):
        if request is None:
            raise Exception('Access Request is None')
        self.controller = self.modem.get_controller()
        self.controller.setup(request)
        self.state = STATE_RING
        self.controller.start()




class HpccInternal(Gate):

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

    def read_state(self):
        is_open = self.magnet_input()
        return STATE_OPEN if is_open else STATE_CLOSED

    def _ip_is_authorized(self, address):
        pattern = getattr(settings, 'IP_PATTERN', '10.87.1.\d+')
        return re.match(pattern, address)
    
    def can_open(self, **kwargs):
        if self.is_open():
            return (False, 'Gate is already open')
        if not 'ip_address' in kwargs or not self._ip_is_authorized(kwargs['ip_address']):
            return (False, 'Ip address not authorized')
        if not 'user' in kwargs or not kwargs['user'].is_staff():
            return (False, 'User has not this capability')
        return (True, None)

    def open_gate(self, request=None):
        if request is None:
            raise Exception('Access Request is None')
        (is_authorized, msg) = self.can_open(user=request.user, ip_address=request.address)
        if not is_authorized:
            request.fail(msg)
            raise Exception(msg)
        self.send_open_pulse()
        request.done()
