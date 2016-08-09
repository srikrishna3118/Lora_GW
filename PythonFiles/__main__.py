import SerialConnection
import glob
import logging
import logging.handlers

LOG_FILE = "syslog_GW.log"
logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)



logging.info('Main:')

connection = SerialConnection.SerialPort('/dev/ttyUSB0',9600)

connection.connect()

print("finish")