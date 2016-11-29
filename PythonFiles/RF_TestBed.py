_author_ = 'Srikrishna'

import sys
import os
import time
import struct
from collections import defaultdict

import RPi.GPIO as GPIO

import Config
import SerialConnection
import SocketListener
from pprint import pprint
import logging
logger = logging.getLogger(__name__)

PARAMETERS = {
    'BAUDRATE':{
        '1':'1200',
        '2':'2400',
        '3':'4800',
        '4':'9600',
        '5':'19200',
        '6':'38400',
        '7':'57600'
    },
    'PARITY':{
        '0':'NONE',
        '1':'ODD',
        '2':'EVEN'
    },
    'RF_FACTOR':{
        '7':'128',
        '8':'256',
        '9':'512',
        '10':'1024',
        '11':'2048',
        '12':'4096'
    },
    'MODE':{
        '0':'STANDARD',
        '1':'CENTRAL',
        '2':'NODE'
    },
    'RF_BW':{
        '6':'62500',
        '7':'125000',
        '8':'256000',
        '9':'500000'
    },
    'RF_POWER':{
        '1':'4dBm',
        '2':'7dBm',
        '3':'10dBm',
        '4':'13dBm',
        '5':'14dBm',
        '6':'17dBm',
        '7': '20dBm'
    }
}

class RF_TestBed:

    def __init__(self):
        # import configuration
        self.config = Config.MyConfiguration('/home/pi/lora/Lora_GW/PythonFiles/lora.conf')
        self.pin = int(self.config.AUX_PIN)
        self.port = self.config.PORT
        self.pingPackets = self.config.TIME
        self.mode = self.config.MODE
        self.module = self.config.MODULE
        self.state = 1
        self.data = ''
        self.command = b"\xAF\xAF\x00\x00\xAF\x80\x02\x0E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9D\x0D\x0A"
        self.cmdResponse = []
        self.pingFlag = 0
        if(self.module=="DORJI"):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.IN)
            self.conn = SerialConnection.SerialPort(self.port, 9600)

        elif(self.module=="IC880A"):
            self.conn = SocketListener.SocketServer(self.port)

    def readEvent(self,channel):
        if (GPIO.input(channel) == 0):
            self.data = self.conn.readline()
            self.pingFlag = 1


    def Run(self):
        logger.info("Testing Begins......")
        print(self.mode)
        if self.mode == "PING":
            self.statistics()
        elif self.mode == "LISTEN":
            self.listener()
        elif self.mode == "CONFIG":
            self.getSettings()


    def listener(self):
        if self.module == "DORJI":
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.readEvent, bouncetime=2)
            logger.info("Module %s",self.module)
            logger.info("Started listening....")
            while(self.state == 1):
                time.sleep(2)

        elif self.module == "IC880A":
            logger.info("Module %s", self.module)
            logger.info("Started listening")
            self.conn.connect()





    def ping(self):
        self.pingFlag = 1
        retries = 3  # retries


        if(self.pingFlag ==1):
            data = "LORA Tx\n"  # b"\xDE\xAD"
            logger.info("Pinging....")
            self.transmitter(data)
            self.pingFlag = 0

            timeout = time.time() + 10
            while True:
                if (GPIO.input(self.pin) == 0) or time.time() > timeout:
                    self.data = self.conn.readline()
                    break

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
            self.conn.writeline(int(data))

    def statistics(self):

        times = int(self.pingPackets)
        track = 0

        while(times > 0):
            result = self.ping()
            if result:
                track = track+1
            times = times-1

        percent = ((int(self.pingPackets) - track)/int(self.pingPackets))*100

        logger.info("RESULT: %s packets received with %s percent package loss", track, percent)


    def getSettings(self):
        logger.info("get the settings from DORJI Lora Radio")
        try:
            self.conn.writecommand(self.command)

            test = 0
            timeout = time.time() + 5 * 5
            while test < 25:

                #if test == 14 or time.time() > timeout:
                data = self.conn.readcmd()
                if data is not None:
                    self.cmdResponse.append(int(data))
                    test =self.cmdResponse.__len__()

            #print self.cmdResponse
            logging.info("results are :")
            #for i in self.cmdResponse:
            #    print i[0]
            logging.info("BAUD RATE     : %s ", PARAMETERS["BAUDRATE"][str(self.cmdResponse[8])])
            logging.info("PARITY        : %s ", PARAMETERS["PARITY"][str(self.cmdResponse[9])])
            frequency = self.cmdResponse[10] << 16 | self.cmdResponse[11] << 8 | self.cmdResponse[12]
            frequency = (float(frequency)*61.035)/1000000  #
            logging.info("FREQUENCY     : %s Mhz", frequency)
            logging.info("RF_FACTOR     : %s ", PARAMETERS["RF_FACTOR"][str(self.cmdResponse[13])])
            logging.info("MODE          : %s ", PARAMETERS["MODE"][str(self.cmdResponse[14])])
            logging.info("RF_BANDWIDTH  : %s ", PARAMETERS["RF_BW"][str(self.cmdResponse[15])])

            device_ID = self.cmdResponse[16] << 8 | self.cmdResponse[17]  # high byte first for 2 bytes device ID
            logging.info("DEVICE ID     : %s", device_ID)
            logging.info("NET_ID        : %s", self.cmdResponse[18])
            logging.info("RF_POWER      : %s", PARAMETERS["RF_POWER"][str(self.cmdResponse[19])])


        except Exception, e:
            logging.error(e, exc_info=True)





    def setValues(self, ID, NetID):
        logger.info("setting following ID: %s and NetID: %s", ID, NetID)

        self.getSettings()

        self.cmdResponse[17] = ID
        self.cmdResponse[18] = NetID
        self.cmdResponse[7] = 1  #write command

        crc = 0
        i = 0
        while i < 22:
            crc =crc + self.cmdResponse[i]
            i=i+1

        crc = int(crc/256)

        self.cmdResponse[23] = crc  # update the crc
        cmd = bytes()
        cmd = cmd.join((struct.pack('B', val) for val in self.cmdResponse))
        try:
            self.conn.writecommand(cmd)
            test = 0
            newcmdResponse = []
            while test < 25:

                #if test == 14 or time.time() > timeout:
                data = self.conn.readcmd()
                if data is not None:
                    newcmdResponse.append(data)
                    test =newcmdResponse.__len__()

            #print self.cmdResponse
            logging.info("results are :")
            #for i in self.cmdResponse:
            #    print i[0]
            logging.info("BAUD RATE     : %s ", PARAMETERS["BAUDRATE"][str(newcmdResponse[8])])
            logging.info("PARITY        : %s ", PARAMETERS["PARITY"][str(newcmdResponse[9])])
            frequency = newcmdResponse[10] << 16 | newcmdResponse[11] << 8 | newcmdResponse[12]
            frequency = (float(frequency)*61.035)/1000000  #
            logging.info("FREQUENCY     : %s Mhz", frequency)
            logging.info("RF_FACTOR     : %s ", PARAMETERS["RF_FACTOR"][str(newcmdResponse[13])])
            logging.info("MODE          : %s ", PARAMETERS["MODE"][str(newcmdResponse[14])])
            logging.info("RF_BANDWIDTH  : %s ", PARAMETERS["RF_BW"][str(newcmdResponse[15])])

            device_ID = int(newcmdResponse[16]) << 8 | int(newcmdResponse[17])  # high byte first for 2 bytes device ID
            logging.info("DEVICE ID     : %s", device_ID)
            logging.info("NET_ID        : %s", newcmdResponse[18])
            logging.info("RF_POWER      : %s", PARAMETERS["RF_POWER"][str(newcmdResponse[19])])
        except Exception, e:
            logging.error(e, exc_info=True)


    def datalogger(self):
        try:
            logger.info("logging Data")

        except Exception, e:
            logger.error(e, exe_info=True)

