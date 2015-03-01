import json
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from gatecontrol import Gate
from models import AccessRequest


class TestViews(TestCase):
    fixtures = ['users.yml']
    
    def setUp(self):
        TestCase.setUp(self)
        setattr(settings, 'GATES', {'test' : Gate() } )
        self.client = Client()
        self.assertTrue(self.client.login(username='admin', password='admin'))
    
    def test_get_all_states(self):
        expected = [{'test' : Gate().get_state(None) }]
        response = self.client.get(reverse('gates'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.dumps(expected), response.content)
        
    def test_gatecontrol(self):
        req_id = {"req_id": 1}
        response = self.client.post(reverse('control', args=('test',)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.dumps(req_id), response.content)
        response = self.client.get(reverse('control', args=('test',)), data=req_id)
        expected = {"pending": True, "description": "closed", "value": 0}
        response = json.loads(response.content)
        self.assertEqual(expected.viewkeys(), response.viewkeys())
        
    def test_show_requests(self):
        self.client.post(reverse('control', args=('test',)))
        pending = AccessRequest.objects.get_pending_request()
        pending.done()
        response = self.client.get(reverse('requests'))
        response = json.loads(response.content)
        expected = {"user": "admin", "time": "2015-03-01T17:28:18"}
        self.assertEqual(expected.viewkeys(), response[0].viewkeys())
        
    


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