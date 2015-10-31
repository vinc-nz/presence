from django.test.testcases import TestCase

from gatecontrol.models import GateController, AccessRequest
from gatecontrol.views import ApiView


class GateControllerStub(GateController):
    
    def __init__(self):
        self.state = 'closed'
    
    def is_managed_by_user(self, user, ip_address):
        return True if user else False
    
    def get_state(self):
        return self.state
    
    def handle_request(self, access_request):
        if self.is_managed_by_user(access_request.user, access_request.address):
            self.state = 'open'
            return True
        return False
        
        
class TestDriven(TestCase):
    
    fixtures = ['gates.yml', 'users.yml']
    
    def setUp(self):
        self.view = ApiView('192.168.1.1')
    
    def test_should_return_the_list_of_gates(self):
        expected = [{
            'id' : 1,
            'name' : 'Testgate',
            'state' : 'closed',
            'managed': False
        }]
        self.assertEqual(expected, self.view.list_gates())
        
    def test_should_authenticate_user(self):
        token = ApiView._create_token('admin')
        self.assertTrue(self.view.authenticate(token))
        
    def test_authenticated_user_should_manage_gate(self):
        token = ApiView._create_token('admin')
        self.view.authenticate(token)
        result = self.view.list_gates()
        self.assertTrue(result[0]['managed'])
        
    def test_authenticated_user_make_an_access_request(self):
        token = ApiView._create_token('admin')
        self.view.authenticate(token)
        self.view.open(1)
        self.assertEqual(1, AccessRequest.objects.all().count())
