
from selfopen import AtlantisModemController, ControllerSkeleton
from django.conf import settings

setattr(settings, 'CONTROLLER_CLASS', ControllerSkeleton)

from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from models import Request
import time

class FakeSerial:
    
    def __init__(self):
        self.last_command = None
        self.next_output = None
    
    def flushInput(self):
        pass
    
    def flushOutput(self):
        pass
    
    def close(self):
        pass
    
    def setTimeout(self, timeout):
        pass
    
    def write(self, command):
        self.last_command = command
        
    def read(self, dontcare):
        return AtlantisModemController.MSG_RING
        
    def readline(self):
        if self.last_command in AtlantisModemController.INIT_COMMANDS:
            self.next_output = AtlantisModemController.MSG_OK 
        elif self.last_command == AtlantisModemController.MSG_OPEN:
            self.next_output = AtlantisModemController.MSG_BUSY
        if self.last_command is not None:
            self.last_command = None
            return 'echo'
        else:
            return self.next_output

def get_fake_serial():
    return FakeSerial()

class TestApp(TestCase):
    
    def testManager(self):
        u = User( id=1, username = 'test' )
        Request.objects.create(u)
        time.sleep(1)
        result = Request.objects.pending_request_present(timedelta(seconds=5))
        self.assertTrue(result)
        
    def testModel(self):
        u = User( id=1, username = 'test' )
        r = Request.objects.create(u)
        r.setup(1)
        r.fullfill()
        
    def testAtlantisModemController(self):
        c = AtlantisModemController(get_fake_serial)
        self.assertTrue(c.setup(1))
        c.run()
        self.assertTrue(c._success)
        
        
        