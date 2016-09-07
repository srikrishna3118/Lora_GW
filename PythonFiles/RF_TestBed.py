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
        self.config = Config.MyConfiguration('/home/pi/lora/Lora_GW/PythonFiles/lora.conf')
        self.pin = int(self.config.AUX_PIN)
        self.port = self.config.PORT
        self.state = 1
        self.data = ''
        self.pingState = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.readEvent)
        self.conn = SerialConnection.SerialPort(self.port, 9600)

    def readEvent(self,channel):
        if (GPIO.input(channel) == 0):
            self.data = self.conn.readline()
        else:
            if (self.pingState):
                self.conn.writeline(self.data)

    def listener(self):
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.writeEvent)
        while(self.state == 1):
            time.sleep(2)

    def ping(self):
        self.pingState = 1
        while(self.state == 1):
            time.sleep(2)

    def transmitter(self,data):
        if(GPIO.input(self.pin)==1):
            self.conn.writeline(data)

    def statistics(self):
        pass

