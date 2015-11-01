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

import asyncio
import sys

import serial, logging


logger = logging.getLogger(__name__)

#constants
MSG_OK =  b'OK\r\n'
MSG_RING = b'\r\nRING\r\n'
MSG_BUSY = b'BUSY\r\n'
MSG_OPEN = b'atdt*\r'

INIT_COMMANDS = (b'at\r', b'atz\r', b'at*nc9\r', b'atx3\r', b'ats11=60\r', b'ats0=0\r')

ECHO_WAIT = 1
INIT_CMD_WAIT = 5

class Modem:

    def get_controller(self):
        pass

class ModemController:

    def setup(self, request, callback=None):
        self.request = request
        self.callback = callback
            
    def on_exit(self):
        if self.callback:
            self.callback()
        
    def handle_ring(self):
        pass

class DummyModem(Modem):

    def get_controller(self):
        return DummyController()


class DummyController(ModemController):

    WAIT = 10

    def setup(self, request, callback=None):
        ModemController.setup(self, request, callback)
        asyncio.get_event_loop().call_later(DummyController.WAIT,  self.on_exit)


class AtlantisModem(Modem):

    PORT = '/dev/ttyUSB0'
    BAUDRATE = 115200


    def _get_serial(self):
        return serial.Serial(AtlantisModem.PORT, baudrate=AtlantisModem.BAUDRATE)

    def check_connection(self):
        s = self._get_serial()
        s.close()
        

    def get_controller(self):
        logger.debug( 'opening serial port..' )
        serial = self._get_serial()
        logger.debug( 'serial port opened' )
        return AtlantisModemController(serial)



class AtlantisModemController(ModemController):


    def __init__(self, serial):
        self.serial = serial

    def add_reader(self):
        loop = asyncio.get_event_loop()
        loop.add_reader(self.serial.fileno(), self.handle_ring)

    def setup(self, request, timeout=60, callback=None):

        ModemController.setup(self, request, callback)

        try:

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
            self.add_reader()
            logger.debug('setup complete, controller in listen mode')
            

        except Exception as e:
            self.serial.close()
            self.request.fail(str(e))
            raise e

    def handle_ring(self):
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
                    logger.debug( 'door opened' )
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
            
        self.on_exit()
            
            
if __name__ == '__main__':
    m=AtlantisModem()
    m.check_connection()
    controller=m.get_controller()
    controller.setup(None)
    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
