_author_ = 'Srikrishna'
import serial
import time
import struct
#import onionGpi
import logging
logger = logging.getLogger(__name__)


class SerialPort(object):

    def __init__(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate
        self.connection = ''
        try:
            self.connection = serial.Serial(port=self.port, baudrate=self.baudrate)
            logger.info("Connected to %s ", self.connection.portstr)
        except:
            logger.error('connection failed')

    def readline(self):
        try:
            bytesToRead = self.connection.inWaiting()
            self.data = self.connection.readline(bytesToRead)
            logger.info("Connected to %s ", self.connection.portstr)
            return self.data
        except:
            logger.error('connection failed')

    def writeline(self, data):
        try:
            self.connection.write(data.encode())
            logger.info('write success')
        except:
            logger.error('write request failed')

