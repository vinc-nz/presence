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

from django.shortcuts import render
from django.conf import settings
import checker
import logging

# import the logging library

# Get an instance of a logger
logger = logging.getLogger('presence')

check = getattr(settings, 'CHECKER_FUNCTION', checker.rpi_gpio_check)

def door_status(request):
    try:
        status = 'Aperto' if check() else 'Chiuso'
        return render(request, 'checker/status.html', {'status' : status })
    except Exception as e:
        logger.error(e)
        return render(request, 'error.html')
    