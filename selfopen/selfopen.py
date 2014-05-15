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

import serial, logging, threading

# Get an instance of a logger
logger = logging.getLogger('presence')



class ControllerSkeleton:
    
    def setup(self, timeout=60):
        self.timeout = timeout
        logger.debug('setting up door controller')
        return True

    def selfopen(self):
        logger.debug('starting opening routine')


def _get_serial():
    return serial.Serial(AtlantisModemController.PORT, baudrate=AtlantisModemController.BAUDRATE)

    
class AtlantisModemController(ControllerSkeleton, threading.Thread):
    
    MSG_OK =  'OK\r\n'
    MSG_RING = '\r\nRING\r\n'
    MSG_BUSY = 'BUSY\r\n'
    MSG_OPEN = 'atdt*\r'
    
    PORT = '/dev/ttyUSB0'
    BAUDRATE = 115200
    
    INIT_COMMANDS = ('at\r', 'atz\r', 'atx3\r', 'ats11=60\r', 'ats0=0\r')
    
    def __init__(self, serial_factory_method=_get_serial):
        self._get_serial = serial_factory_method
        self._success = False
    
    def setup(self, timeout=60):
        ControllerSkeleton.setup(self, timeout=timeout)
        
        logger.debug( 'opening serial port..' )
        try:
            self.serial = self._get_serial()
            self.serial.setTimeout(timeout)
        except Exception:
            logger.error( 'error opening serial')
            return False
        
        logger.debug( 'flushing buffers' )
        self.serial.flushInput()
        self.serial.flushOutput() 
        
        logger.debug( 'sending init commands to modem..' )
        for c in AtlantisModemController.INIT_COMMANDS:
            self.serial.write(c)
            self.serial.readline() #echo
            if self.serial.readline() != AtlantisModemController.MSG_OK:
                logger.error( 'error at comand: %s' % c )
                self.serial.close()
                return False
            
        logger.debug('setup complete, controller in listen mode')
        return True
    
    def run(self):
        logger.debug( 'modem in ascolto' )
    
        lineIn = self.serial.read(len(AtlantisModemController.MSG_RING))
        if lineIn == AtlantisModemController.MSG_RING:
            logger.debug( 'RING received' )
            logger.debug( 'sending *' )
            self.serial.write(AtlantisModemController.MSG_OPEN)
            while lineIn != AtlantisModemController.MSG_BUSY and len(lineIn) > 0:
                lineIn = self.serial.readline()
            if lineIn == AtlantisModemController.MSG_BUSY:
                logger.info( 'door opened' )
                self._success = True
            else:
                logger.error('unknow error, doing nothing')
        else:
            logger.debug( 'invalid input: %s' % lineIn )
        
        logger.debug( 'closing serial port' )
        self.serial.close()
        
    def selfopen(self):
        ControllerSkeleton.selfopen(self)
        self.start()
        
        
    





