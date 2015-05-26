
import datetime
import logging

from django.contrib.auth.models import User
from django.db import models


logger = logging.getLogger(__name__)

REQUEST_STATE_PENDING = 'PENDING'
REQUEST_STATE_OK = 'OK'
REQUEST_STATE_FAIL = 'FAIL'


class RequestManager(models.Manager):
    
    def get_or_create(self, user, address, gate, gate_name):
        access_request = self.get_pending_request(gate_name)
        if access_request is None:
            logger.info('user %s requested access' % user.username)
            access_request = AccessRequest( user = user, gate=gate_name, address=address, req_time = datetime.datetime.now(), req_state = REQUEST_STATE_PENDING )
            gate.open_gate(access_request)
            access_request.save()
        return access_request
    
    def get_last_accesses(self, gate_name, limit=10):
        return self.filter(req_state=REQUEST_STATE_OK, gate=gate_name).order_by('-req_time')[:limit]

    def get_pending_request(self, gate_name):
        results = self.filter(req_state=REQUEST_STATE_PENDING, gate=gate_name)
        return results[0] if len(results) > 0 else None
        


class AccessRequest(models.Model):
    user = models.ForeignKey(User)
    req_time = models.DateTimeField()
    req_state = models.TextField()
    info = models.TextField()
    gate = models.TextField(default='unknown')
    address = models.TextField(default='unknown')
    objects = RequestManager()
    
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
    
