import RF_TestBed
import glob
import logging
import logging.handlers
#import PythonFiles.SerialConnection as Conn

LOG_FILE = "syslog_GW.log"
logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)



logging.info('Main:')

Test = RF_TestBed.RF_TestBed()

#Test.listener()
Test.ping()

print("finish")