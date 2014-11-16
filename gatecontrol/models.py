
import datetime
import logging

from django.contrib.auth.models import User
from django.db import models


logger = logging.getLogger('gatecontrol')

REQUEST_STATE_PENDING = 'PENDING'
REQUEST_STATE_OK = 'OK'
REQUEST_STATE_FAIL = 'FAIL'


class RequestManager(models.Manager):
    
    def create(self, user):
        logger.info('user %s requested access' % user.username)
        r = AccessRequest( user = user, req_time = datetime.datetime.now(), req_state = REQUEST_STATE_PENDING )
        r.save()
        return r
    
    def get_last_accesses(self, limit=10):
        return self.filter(req_state=REQUEST_STATE_OK).order_by('-req_time')[:limit]

    def get_pending_request(self):
        results = self.filter(req_state=REQUEST_STATE_PENDING)
        return results[0] if len(results) > 0 else None
        


class AccessRequest(models.Model):
    user = models.ForeignKey(User)
    req_time = models.DateTimeField()
    req_state = models.TextField()
    info = models.TextField()
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
    
