_author_ = 'Srikrishna'

import os
import time
import RPi.GPIO as GPIO

import Config
import SerialConnection

import logging
logger = logging.getLogger(__name__)

class RF_TestBed:


    def __init__(self):
        # import configuration
        self.config = Config.MyConfiguration('lora.conf')
        self.pin = self.config.AUX_PIN
        self.port = self.config.PORT
        self.state = 1
        self.data = ''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(12, GPIO.FALLING, callback=self.readEvent)
        self.connection = SerialConnection.SerialPort(self.port, 9600)

    def readEvent(self,channel):
        if (GPIO.input(channel) == 0):
            self.data = self.connection.readline()

    def listener(self):
        while(self.state == 1):
            time.sleep(2)

    def ping(self):
        if(GPIO.input(self.pin)==1):
            self.connection.writeline(self.data)

    def transmitter(self,data):
        if(GPIO.input(self.pin)==1):
            self.connection.writeline(data)

    def statistics(self):
        pass
