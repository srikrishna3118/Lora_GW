_author_ = 'Srikrishna'

import os
import serial, time
import RPi.GPIO as GPIO

import Config



class RF_TestBed:


    def __init__(self, opts):
        # import configuration
        self.config = Config.MyConfiguration('lora.conf')
        self.pin = self.config.AUX_PIN
        self.port = self.config.PORT
        self.state = 1
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(12, GPIO.FALLING, callback=readEvent)

    def readEvent(self,channel):
        if (GPIO.input(channel) == 0):
            self.data = self.port.readline()

    def listener(self):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=readEvent)
        while(self.state == 1):
            time.sleep(2)

    def ping(self):
        if(GPIO.input(self.pin)==1):
            self.port.write(self.data)

    def transmitter(self,data):
        if(GPIO.input(self.pin)==1):
            self.port.write(data)

    def statistics(self):
        pass
