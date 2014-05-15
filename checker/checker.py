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