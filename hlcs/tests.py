
from unittest.mock import Mock, MagicMock

from django.test import TestCase
from serial.serialutil import SerialException
from serial import Serial

from hlcs import modem
from hlcs.modem import AtlantisModem


class TestAtlantisModemController(TestCase):
    
    def testDone(self):
        request = Mock()
        serial = Mock()
        serial.readline = MagicMock(return_value=modem.MSG_OK)
        controller = modem.AtlantisModemController(serial)
        controller.setup(request)
        serial.read = MagicMock(return_value=modem.MSG_RING)
        serial.readline = MagicMock(return_value=modem.MSG_BUSY)
        controller.run()
        request.done.assert_called_with()
        
    def testFail(self):
        request = Mock()
        
        try:
            serial = Serial(AtlantisModem.PORT, baudrate=AtlantisModem.BAUDRATE)
        except SerialException:
            serial = Mock()
            serial.readline = MagicMock(return_value=modem.MSG_OK)
            serial.read = MagicMock(return_value=None)
            
        controller = modem.AtlantisModemController(serial)
        controller.setup(request)
        controller.run()
        request.fail.assert_called_with('no RING received')
