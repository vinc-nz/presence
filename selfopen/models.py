from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import selfopen


controller_class = getattr(settings, 'CONTROLLER_CLASS', selfopen.AtlantisModemController)


class RequestManager(models.Manager):
    
    def create(self, user):
        r = Request( user = user, req_time = timezone.now() )
        r.save()
        r.set_controller(controller_class())
        return r
    
    def pending_request_present(self, timedelta):
        time_threshold = datetime.now() - timedelta
        results = self.filter(req_time__gt=time_threshold)
        return True if len(results) > 0 else False
        


class Request(models.Model):
    user = models.ForeignKey(User)
    req_time = models.DateTimeField()
    objects = RequestManager()
    
    def set_controller(self, controller):
        self.controller = controller
    
    def setup(self, timeout=60):
        return self.controller.setup(timeout)

    def fullfill(self):
        self.controller.selfopen()
    
