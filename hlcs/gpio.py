'''
Created on 08/nov/2014

@author: spax
'''
import logging

import RPi.GPIO as GPIO
from time import sleep
from django.conf import settings


logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)

LOCK_PIN = getattr(settings, 'LOCK_PIN', 4)
MAGNET_PIN = getattr(settings, 'MAGNET_PIN', 17)

PULSE_SLEEP = getattr(settings, 'PULSE_SLEEP', 1)
PULSE_ON = getattr(settings, 'PULSE_ON', 1)
PULSE_OFF = getattr(settings, 'PULSE_OFF', 0)

GPIO.setup(LOCK_PIN, GPIO.OUT, initial=PULSE_OFF)
GPIO.setup(MAGNET_PIN, GPIO.IN)  
    


def magnet_input():
    try:
        return GPIO.input(MAGNET_PIN)
    except Exception as e:
        logger.exception(e)
        return False
    

def send_open_pulse():
    try:
        GPIO.output(MAGNET_PIN, PULSE_ON)
        sleep(PULSE_SLEEP)
        GPIO.output(MAGNET_PIN, PULSE_OFF)
    except Exception as e:
        logger.exception(e)
    




    