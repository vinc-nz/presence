
import datetime
import logging

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings as settings


logger = logging.getLogger(__name__)

REQUEST_STATE_PENDING = 'PENDING'
REQUEST_STATE_OK = 'OK'
REQUEST_STATE_FAIL = 'FAIL'


class RequestManager(models.Manager):

    def get_or_create(self, user, address, gate_name):
        gates = getattr(settings, 'GATES')
        gate = gates[gate_name]
        logger.info('user %s requested access' % user.username)
        access_request = AccessRequest( user = user, gate=gate_name, address=address, req_time = datetime.datetime.now(), req_state = REQUEST_STATE_PENDING )
        gate.open_gate(access_request)
        access_request.save()
        return access_request

    def get_last_accesses(self, gate_name, limit=10):
        return self.filter(req_state=REQUEST_STATE_OK, gate=gate_name).order_by('-req_time')[:limit]





class AccessRequest(models.Model):
    user = models.ForeignKey(User)
    req_time = models.DateTimeField()
    req_state = models.TextField()
    info = models.TextField()
    gate = models.TextField()
    address = models.TextField(null=True)
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
