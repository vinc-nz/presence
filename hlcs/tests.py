
from django.test import TestCase

from hlcs.atlantis import FakeRequest, AtlantisModemController


class TestAtlantisModemController(TestCase):
    
    def test(self):
        request = FakeRequest()
        controller = AtlantisModemController(test_env=True)
        controller.setup(request)
        controller.run()
        self.assertTrue(request.success)
