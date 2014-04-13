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

import serial

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('presence')



def test(timeout=60, port='/dev/ttyUSB0', baudrate=115200 ):
    logger.debug('chiamato metodo di test con parametri (%s, %d, %d)' % (port, baudrate, timeout) )

def selfopen(timeout=60, port='/dev/ttyUSB0', baudrate=115200 ):
    
    #costanti
    OK =  'OK\r\n'
    RING = '\r\nRING\r\n'
    BUSY = 'BUSY\r\n'

    logger.debug( 'apro la seriale' )
    s = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    ## TODO gestire eccezione
    
    logger.debug( 'svuoto i buffer' )
    s.flushInput() #flush input buffer, discarding all its contents
    s.flushOutput()#flush output buffer, aborting current output 
    
    
    init_commands = ('at', 'atz', 'atx3', 'ats11=60', 'ats0=0')
    logger.debug( 'invio i comandi di inizializzazione' )
    for c in init_commands:
        s.write(c + '\r')
        s.readline() #echo
        if not s.readline() == OK:
            logger.debug( 'errore al comando %s' % c )
            s.close()
            #TODO da gestire
        
    
    logger.debug( 'modem in ascolto' )
    
    lineIn = s.read(len(RING))
    if lineIn == RING:
        logger.debug( 'ricevuto RING' )
        logger.debug( 'invio *' )
        s.write('atdt*\r')
        while lineIn != BUSY:
            lineIn = s.readline()
            #TODO gestire timeout della readline
        logger.info( 'porta aperta' )
    else:
        logger.debug( 'ricevuto input non valido' )
    
    logger.debug( 'chiudo la seriale' )
    s.close()




