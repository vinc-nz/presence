
import importlib
import logging

from django.contrib.auth.models import User
from django.db import models


logger = logging.getLogger(__name__)

REQUEST_STATE_PENDING = 'PENDING'
REQUEST_STATE_OK = 'OK'
REQUEST_STATE_FAIL = 'FAIL'

GATE_STATE_OPEN = 'open'
GATE_STATE_CLOSED = 'closed'


class Gate(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    controller_class = models.CharField(max_length=100)
    
    def controller(self):
        module_name, class_name = self.controller_class.rsplit(".", 1)
        ControllerClass = getattr(importlib.import_module(module_name), class_name)
        return ControllerClass()
    
    def request_opening(self, user, client):
        logger.info('user %s requested access' % user.username)
        gate_controller = self.controller()
        if gate_controller.is_managed_by_user(user, client):
            access_request = AccessRequest( user = user, gate=self )
            access_request.set_client(client)
            try:
                gate_controller.handle_request(access_request)
                access_request.save()
                return True
            except Exception as e:
                access_request.fail(str(e))
                access_request.save()
                raise e
        raise Exception('Unauthorized')
        
    def get_last_accesses(self, limit):
        self.accessrequest.filter(req_state=REQUEST_STATE_OK).order_by('-req_time')[:limit]
    


class AccessRequest(models.Model):
    user = models.ForeignKey(User)
    req_time = models.DateTimeField(auto_now=True)
    req_state = models.TextField(default=REQUEST_STATE_PENDING)
    info = models.TextField()
    gate = models.ForeignKey(Gate)
    address = models.TextField(null=True)
    
    def set_client(self, client):
        self.client = client
        self.address = client.request.remote_ip
        logger.info('request from {}'.format(self.address))

    def done(self):
        self.req_state = REQUEST_STATE_OK
        self.save()

    def fail(self, msg):
        self.req_state = REQUEST_STATE_FAIL
        self.info = msg
        self.save()

    def is_ok(self):
        return self.req_state == REQUEST_STATE_OK

    def is_pending(self):
        return self.req_state == REQUEST_STATE_PENDING


class GateController(object):
    
    def is_managed_by_user(self, user, client):
        raise NotImplementedError()
    
    def get_state(self):
        raise NotImplementedError()
    
    def handle_request(self, access_request):
        raise NotImplementedError()


