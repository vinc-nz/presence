"""
Copyright (C) 2014, Vincenzo Pirrone <pirrone.v@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import Request
import logging

# import the logging library

# Get an instance of a logger
logger = logging.getLogger('presence')

WAIT_TIMEOUT = 60

# Create your views here.
@login_required
def wait_ring(request):
    logger.info('USER %s REQUESTS ACCESS' % request.user.username)
    
    if not Request.objects.pending_request_present(timedelta(seconds=WAIT_TIMEOUT)):
        logger.info('request from %s accepted' % request.user.username )
        selfopen_request = Request.objects.create(request.user)
        if selfopen_request.setup(WAIT_TIMEOUT):
            selfopen_request.fullfill()
            return render(request, 'selfopen/waiting.html', {'timeout' : WAIT_TIMEOUT})
        else:
            return render(request, 'selfopen/error.html')
    else:
        return render(request, 'selfopen/concurrency.html')
    
    