import time

from django.contrib.auth.models import User
from django.test import TestCase

from models import AccessRequest


class TestManager(TestCase):
    
    def test_get_pending_request(self):
        u = User( id=1, username = 'test' )
        u.save()
        r1 = AccessRequest.objects.create(u)
        self.assertEquals(r1, AccessRequest.objects.get_pending_request())
        
    def test_get_last_accesses(self):
        u = User( id=1, username = 'test' )
        u.save()
        r1 = AccessRequest.objects.create(u)
        r1.done()
        time.sleep(1)
        r2 = AccessRequest.objects.create(u)
        r2.done()
        accesses = [a.id for a in AccessRequest.objects.get_last_accesses()]
        self.assertEquals( [r2.id, r1.id], accesses)