import json
import time
from unittest.mock import MagicMock

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from gatecontrol.gatecontrol import Gate, STATE_CLOSED
from gatecontrol.models import AccessRequest


class TestViews(TestCase):
    fixtures = ['users.yml', 'requests.yml']
    
    def parse_response(self, response):
        self.assertEqual(200, response.status_code)
        return json.loads(response.content.decode(response._charset))
    
    def setUp(self):
        TestCase.setUp(self)
        mock = Gate()
        mock.get_state = MagicMock(return_value=STATE_CLOSED)
        mock.open_gate = MagicMock()
        setattr(settings, 'GATES', {'test' : mock } )
        self.client = Client()
        self.assertTrue(self.client.login(username='admin', password='admin'))
    
    def test_get_all_states(self):
        expected = [{'test' : STATE_CLOSED }]
        response = self.client.get(reverse('gates'))
        actual = self.parse_response(response)
        self.assertEqual(expected, actual)
        
    def test_gatecontrol(self):
        expected = {"req_id": 2}
        response = self.client.post(reverse('control', args=('test',)))
        req_id = self.parse_response(response)
        self.assertEqual(expected, req_id)
        response = self.client.get(reverse('control', args=('test',)), data=req_id)
        expected = {"description": "closed", "id": 0}
        actual = self.parse_response(response)
        self.assertEqual(expected.keys(), actual.keys())
        
    def test_show_requests(self):
        response = self.client.get(reverse('requests'))
        actual = self.parse_response(response)[0]
        expected = {"user": "admin", "time": "2015-03-01T17:28:18"}
        self.assertEqual(expected.keys(), actual.keys())
        
    


class TestManager(TestCase):
    fixtures = ['users.yml']
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
    
    def test_get_pending_request(self):
        r1 = AccessRequest.objects.create(self.user)
        self.assertEquals(r1, AccessRequest.objects.get_pending_request())
        
    def test_get_last_accesses(self):
        u = self.user
        r1 = AccessRequest.objects.create(u)
        r1.done()
        time.sleep(1)
        r2 = AccessRequest.objects.create(u)
        r2.done()
        accesses = [a.id for a in AccessRequest.objects.get_last_accesses()]
        self.assertEquals( [r2.id, r1.id], accesses)