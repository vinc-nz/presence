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

import sys
import threading, time
import unittest

import serial, logging


logger = logging.getLogger(__name__)

#constants
MSG_OK =  'OK\r\n'
MSG_RING = '\r\nRING\r\n'
MSG_BUSY = 'BUSY\r\n'
MSG_OPEN = 'atdt*\r'
    
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
    
INIT_COMMANDS = ('at\r', 'atz\r', 'at*nc9\r', 'atx3\r', 'ats11=60\r', 'ats0=0\r')
    
ECHO_WAIT = 1
INIT_CMD_WAIT = 5



class FakeSerial:
    
    READ_TIMEOUT = 60
    
    def __init__(self):
        self.last_command = None
        self.next_output = None
    
    def flushInput(self):
        pass
    
    def flushOutput(self):
        pass
    
    def close(self):
        pass
    
    def setTimeout(self, timeout):
        pass
    
    def write(self, command):
        self.last_command = command
        
    def read(self, dontcare):
        time.sleep(FakeSerial.READ_TIMEOUT)
        return MSG_RING
        
    def readline(self):
        if self.last_command in INIT_COMMANDS:
            self.next_output = MSG_OK 
        elif self.last_command == MSG_OPEN:
            self.next_output = MSG_BUSY
        if self.last_command is not None:
            self.last_command = None
            return 'echo'
        else:
            return self.next_output
        

class FakeRequest:
    
    def __init__(self):
        self.success = False
        
    def done(self):
        self.success = True
        
    def fail(self, msg):
        pass



def _get_serial():
    return serial.Serial(PORT, baudrate=BAUDRATE)

def check_modem():
    try:
        s = _get_serial()
        s.close()
    except Exception as e:
        print ('ERROR: %s: %s' % (__name__, str(e)))
        sys.exit(1)

def _stub_serial():
    return FakeSerial()
    
class AtlantisModemController(threading.Thread):
    
    
    def __init__(self, test_env=False):
        threading.Thread.__init__(self)
        if test_env:
            self._get_serial = _stub_serial
        else:
            self._get_serial = _get_serial
    
    
    def setup(self, request, timeout=60):
        
        self.request = request
        
        try:
        
            logger.debug( 'opening serial port..' )
            self.serial = self._get_serial()
            self.serial.setTimeout(INIT_CMD_WAIT)
            
            logger.debug( 'flushing buffers' )
            self.serial.flushInput()
            self.serial.flushOutput() 
            
            logger.debug( 'sending init commands to modem..' )
            for c in INIT_COMMANDS:
                logger.debug( 'sending %s' % c )
                self.serial.write(c)
                logger.debug( 'reading echo'  )
                echo = self.serial.readline() #echo
                if len(echo)==0:
                    raise IOError( 'no echo received')
                else:
                    ok = self.serial.readline()
                    if ok != MSG_OK:
                        raise IOError( 'error at comand: %s' % c )
            
            self.serial.setTimeout(timeout)   
            logger.debug('setup complete, controller in listen mode')
            
        except Exception as e:
            try:
                self.serial.close()
            except Exception:
                pass
            logger.exception(e)
            self.request.fail(str(e))
    
    def run(self):
        try:
            logger.debug( 'modem in listen mode' )
        
            lineIn = self.serial.read(len(MSG_RING))
            if lineIn == MSG_RING:
                logger.debug( 'RING received' )
                logger.debug( 'sending *' )
                self.serial.write(MSG_OPEN)
                while lineIn != MSG_BUSY and len(lineIn) > 0:
                    lineIn = self.serial.readline()
                    logger.debug( 'modem: %s' % lineIn.rstrip() )
                if lineIn == MSG_BUSY:
                    logger.info( 'door opened' )
                    self.request.done()
                else:
                    msg = 'invalid input: %s' % lineIn.rstrip()
                    logger.error( msg )
                    self.request.info = msg
            else:
                msg = 'no RING received'
                logger.debug( msg )
                self.request.fail(msg)
            
            logger.debug( 'closing serial port' )
            self.serial.close()
        except Exception as e:
            logger.exception(e)
            self.request.fail(str(e))
        
        

        






