import json
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from mock import MagicMock
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from gatecontrol.gatecontrol import Gate, STATE_CLOSED
from gatecontrol.models import AccessRequest


class TestViews(APITestCase):
    fixtures = ['users.yml', 'requests.yml']
    
    def parse_response(self, response):
        self.assertEqual(200, response.status_code)
        return json.loads(response.content.decode())
    
    def setUp(self):
        APITestCase.setUp(self)
        mock = Gate()
        mock.get_state = MagicMock(return_value=STATE_CLOSED)
        mock.open_gate = MagicMock()
        setattr( settings, 'GATES', {'test' : mock } )
        self.client.force_authenticate(user=User.objects.get(pk=1))
    
    def test_gatecontrol(self):
        expected = {"req_state": 'PENDING'}
        response = self.client.post(reverse('control', args=('test',)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, self.parse_response(response))
        
    def test_show_requests(self):
        response = self.client.get(reverse('requests',  args=('test',) ))
        self.assertEqual(200, response.status_code)
        actual = self.parse_response(response)[0]
        expected = {"user": "admin", "time": "2015-03-01T17:28:18"}
        self.assertEqual(expected.keys(), actual.keys())
        
    def test_show_user_capabilities(self):
        response = self.client.get(reverse('capabilities' ))
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.dumps({'test' : True}), response.content.decode())
        
    

class TestManager(TestCase):
    fixtures = ['users.yml', 'requests.yml']
    
    def setUp(self):
        TestCase.setUp(self)
        
    def test_get_last_accesses(self):
        accesses = AccessRequest.objects.get_last_accesses('test')
        self.assertEqual([1], [a.id for a in accesses])
