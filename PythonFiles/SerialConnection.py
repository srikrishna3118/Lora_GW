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
        self.data = ''
        self.command = b"\xAF\xAF\x00\x00\xAF\x80\x02\x0E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9D\x0D\x0A"
        try:
            self.connection = serial.Serial(port=self.port, baudrate=self.baudrate)
            logger.info("Connected to %s ", self.connection.portstr)
        except:
            logger.error('connection failed')

    def readline(self):
        try:
            #bytesToRead = self.connection.inWaiting()
            self.data = self.connection.readline()
            logger.info("data received: %s ", self.data)
            return self.data
        except:
            logger.error('read request failed')

    def writeline(self, data):
        try:
            self.connection.write(data.encode())
            logger.info('data: %s write success', data)
        except:
            logger.error('write request failed')

    def writecommand(self,cmd):
        pass

