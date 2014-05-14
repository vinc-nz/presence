from django.contrib.auth.models import User
from django.test import TestCase
from selfopen.models import Request

class ManagerTest(TestCase):
    
    def test(self):
        Request.objects.create()