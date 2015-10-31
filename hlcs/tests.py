


from unittest.mock import MagicMock

from django.test import TestCase
from serial import Serial
from serial.serialutil import SerialException

from hlcs import modem
from hlcs.modem import AtlantisModem


class TestAtlantisModemController(TestCase):
    
    def testDone(self):
        request = MagicMock()
        serial = MagicMock()
        serial.readline = MagicMock(return_value=modem.MSG_OK)
        controller = modem.AtlantisModemController(serial)
        controller.add_reader = MagicMock()
        controller.setup(request)
        serial.read = MagicMock(return_value=modem.MSG_RING)
        serial.readline = MagicMock(return_value=modem.MSG_BUSY)
        controller.handle_ring()
        request.done.assert_called_with()
        
    def testFail(self):
        request = MagicMock()
        
        try:
            serial = Serial(AtlantisModem.PORT, baudrate=AtlantisModem.BAUDRATE)
        except SerialException:
            serial = MagicMock()
            serial.readline = MagicMock(return_value=modem.MSG_OK)
            serial.read = MagicMock(return_value=None)
            
        controller = modem.AtlantisModemController(serial)
        controller.add_reader = MagicMock()
        controller.setup(request)
        controller.handle_ring()
        request.fail.assert_called_with('no RING received')
