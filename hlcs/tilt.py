'''
Created on 08/nov/2014

@author: spax
'''
import logging

import RPi.GPIO as GPIO


logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)
LOCK_PIN=8
GPIO.setup(LOCK_PIN, GPIO.IN) 
    


def rpi_gpio_check():
    try:
        return True if GPIO.input(LOCK_PIN) else False
    except Exception as e:
        logger.exception(e)
        return False
    




    