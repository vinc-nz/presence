'''
Created on 08/nov/2014

@author: spax
'''
import logging

import RPi.GPIO as GPIO
from time import sleep
from django.conf import settings



GPIO.setmode(GPIO.BCM)

LOCK_PIN = getattr(settings, 'LOCK_PIN', 4)
MAGNET_PIN = getattr(settings, 'MAGNET_PIN', 17)

PULSE_SLEEP = getattr(settings, 'PULSE_SLEEP', 1)
PULSE_ON = getattr(settings, 'PULSE_ON', 0)
PULSE_OFF = getattr(settings, 'PULSE_OFF', 1)


def setup():
    GPIO.setup(LOCK_PIN, GPIO.OUT, initial=PULSE_OFF)
    GPIO.setup(MAGNET_PIN, GPIO.IN)  


def magnet_input():
    return GPIO.input(MAGNET_PIN)
    

def send_open_pulse():
    GPIO.output(LOCK_PIN, PULSE_ON)
    sleep(PULSE_SLEEP)
    GPIO.output(LOCK_PIN, PULSE_OFF)
    




    