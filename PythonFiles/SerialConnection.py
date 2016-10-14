_author_ = 'Srikrishna'

import sys
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
        try:
            self.connection = serial.Serial(port=self.port, baudrate=self.baudrate)
            logger.info("Connected to %s ", self.connection.portstr)
        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('connection failed')

    def readline(self):
        try:
            #bytesToRead = self.connection.inWaiting()
            self.data = self.connection.readline()
            logger.info("data received: %s ", self.data)
            return self.data
        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('read request failed')

    def readcmd(self):
        try:
            if (self.connection.inWaiting()):
                self.data = self.connection.read()
                resp = struct.unpack("!B", self.data)[0]
                #logging.info("DATA %s",resp)
                return resp
                return self.data


        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('read request failed')

    def writeline(self, data):
        try:
            self.connection.write(data.encode())
            logger.info('data: %s write success', data)
        except:
            logger.error('write request failed')

    def writecommand(self,cmd):
        try:
            if cmd is not None:
                logging.info("command sequence: %s executed",cmd)
                self.connection.write(cmd)

        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('write request failed')

