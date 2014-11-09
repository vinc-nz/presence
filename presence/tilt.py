'''
Created on 08/nov/2014

@author: spax
'''
from django.conf import settings
from gatecontrol.gatecontrol import STATE_OPEN, STATE_CLOSED


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    LOCK_PIN=8
    GPIO.setup(LOCK_PIN, GPIO.IN) 
    
    def rpi_gpio_check():
        return True if GPIO.input(LOCK_PIN) else False
    
except Exception as e:
    
    def rpi_gpio_check():
        raise RuntimeError('error setting up GPIO')


def stub_check():
    #shoud return True if door is open, false otherwise
    return False

def read_tilt_state():
    check = getattr(settings, 'TILT_CHECKER', rpi_gpio_check)
    return STATE_OPEN if check() else STATE_CLOSED
    