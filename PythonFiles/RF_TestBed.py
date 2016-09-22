_author_ = 'Srikrishna'

import os
import time
import struct

import RPi.GPIO as GPIO

import Config
import SerialConnection

import logging
logger = logging.getLogger(__name__)

class RF_TestBed:

    def __init__(self):
        # import configuration
        self.config = Config.MyConfiguration('/home/pi/lora/Lora_GW/PythonFiles/lora.conf')
        self.pin = int(self.config.AUX_PIN)
        self.port = self.config.PORT
        self.pingPackets = self.config.TIME
        self.mode = self.config.MODE
        self.state = 1
        self.data = ''
        self.cmdResponse =''
        self.pingFlag = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.readEvent)
        self.conn = SerialConnection.SerialPort(self.port, 9600)

    def readEvent(self,channel):
        if (GPIO.input(channel) == 0):
            self.data = self.conn.readline()
            self.pingFlag = 1


    def listener(self):
        logger.info("Started listening....")
        while(self.state == 1):
            time.sleep(2)

    def ping(self):
        self.pingFlag = 1
        retries = 3  # retries

        #listener thread started.
        #self.listener()

        if(self.pingFlag ==1):
            data = "ALIVE\n"  # b"\xDE\xAD"
            logger.info("Pinging....")
            self.transmitter(data)
            self.pingFlag = 0

            time.sleep(2)
            while(retries>0):
                if self.data is not None:
                    if(self.data == data):
                        logger.info("PING SUCCESS %d ", retries)
                        retries = 0
                        return 1
                    else:
                        retries = retries-1

            if self.data is None:
                return 0




    def transmitter(self,data):
        if(GPIO.input(self.pin)==1):
            self.conn.writeline(data)

    def statistics(self):

        times = int(self.pingPackets)
        track = 0

        while(times > 0):
            result = self.ping()
            if result:
                track = track+1
            times = times-1

        percent = ((track - int(self.pingPackets))/int(self.pingPackets))*100

        logger.info("RESULT: %s packets received with %s percent package loss", track, percent)






