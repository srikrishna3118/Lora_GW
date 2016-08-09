import serial
import time
import struct
#import onionGpio

import logging


logger = logging.getLogger(__name__)


class SerialPort(object):

    def __init__(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate

    def connect(self):

        try:
            self.connection = serial.Serial(port=self.device, baudrate=self.baudrate)
            logger.info('Connected to ', self.connection.portstr)
        except:
            logger.error('connection failed')
            logger.error(self.connection.portstr)

    def readline(self):
        try:
            bytesToRead = self.connection.inWaiting()
            self.data = SerialPort.read(bytesToRead)
            logger.info('received data:', self.data)
            return self.data
        except:
            logger.error('connection failed')

    def writeline(self, data):
        try:
            SerialPort.write(data.encode())
            logger.info('write success')
        except:
            logger.error('write request failed')
