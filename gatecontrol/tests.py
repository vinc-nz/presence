from functools import partial
from functools import partial
import json
from unittest.mock import MagicMock, Mock

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.staticfiles import testing
from django.test.testcases import TestCase
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from ws4py.client.tornadoclient import TornadoWebSocketClient

from gatecontrol.handlers import SocketHandler, TokenHandler
from gatecontrol.models import GateController, AccessRequest
from gatecontrol.views import ApiView


class GateControllerStub(GateController):
    
    def __init__(self):
        self.state = 'closed'
    
    def is_managed_by_user(self, user, client):
        return True if user else False
    
    def get_state(self):
        return self.state
    
    def handle_request(self, access_request):
        if self.is_managed_by_user(access_request.user, access_request.client):
            self.state = 'open'
            return True
        return False
        
        
class TestApi(TestCase):
    
    fixtures = ['gates.yml', 'users.yml']
    
    def setUp(self):
        client = Mock(request=Mock(remote_ip='192.168.1.1'))
        self.view = ApiView(client)
    
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
        
        

class AsyncWSClient(TornadoWebSocketClient):


    def __init__(self, url, ioLoop=None, **kwargs):
        TornadoWebSocketClient.__init__(self, url, io_loop=ioLoop, **kwargs)
        self._callback = None
        self._message = None
    
    def opened(self):
        """called when web socket opened"""
        self.send(self._message, binary=False)      
    
    def received_message(self, message):
        """Received a message"""
        self.close()
        if self._callback:
            self._callback(message.data)
    
    def sendMessage(self, message, callback):
        """Connects and sends message when connected"""
        self._message = message
        self._callback = callback
        self.connect()

"""
class WebSocketTest(AsyncHTTPTestCase):
    
    @classmethod
    def setUpClass(cls):
        super(WebSocketTest, cls).setUpClass()
        user = User.objects.create(username='test')
        user.set_password('secret')
        user.save()
    
    def get_app(self):
        return Application([('/token', TokenHandler), ('/socket', SocketHandler)])

    def test_should_return_the_list_of_gates(self):
        url = self.get_url('/socket').replace('http', 'ws')
        client = AsyncWSClient(url, self.io_loop)
        client.sendMessage(json.dumps({'method': 'list_gates', 'args': {}}), self.stop)

        response = json.loads(self.wait().decode())
        self.assertEqual({'type': 'list_gates', 'content': []}, response)
        
    def test_should_issue_token(self):
        auth_request = {'username': 'test', 'password': 'secret'}
        self.http_client.fetch(self.get_url('/token'), self.stop, method="POST", body=json.dumps(auth_request))
        response = json.loads(self.wait().body.decode())
        self.assertEqual('token', response['type'])
        
    def test_should_authenticate_user(self):
        url = self.get_url('/socket').replace('http', 'ws')
        client = AsyncWSClient(url, self.io_loop)
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.FILrByQNl1Mx00RSZonmT3p5waGlFaymZJ3e3a5VBac'
        client.sendMessage(json.dumps({'method': 'authenticate', 'args': {'token': token}}), self.stop)
        response = json.loads(self.wait().decode())
        self.assertEqual({'type': 'authenticate', 'content': 'success'}, response)

"""
