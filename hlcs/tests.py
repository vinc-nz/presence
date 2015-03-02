
from unittest.mock import Mock, MagicMock

from django.test import TestCase

from hlcs import modem


class TestAtlantisModemController(TestCase):
    
    def test(self):
        request = Mock()
        serial = Mock()
        serial.readline = MagicMock(return_value=modem.MSG_OK)
        controller = modem.AtlantisModemController(serial)
        controller.setup(request)
        serial.read = MagicMock(return_value=modem.MSG_RING)
        serial.readline = MagicMock(return_value=modem.MSG_BUSY)
        controller.run()
        request.done.assert_called_with()
