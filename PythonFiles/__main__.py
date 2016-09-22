import RF_TestBed
import glob
import logging
import logging.handlers


LOG_FILE = "syslog_GW.log"
logging.basicConfig(format='%(asctime)s %(message)s',filename=LOG_FILE,level=logging.DEBUG)



logging.info('Main:Started')

Test = RF_TestBed.RF_TestBed()

#Test.transmitter("hi buddy")
#Test.listener()
#Test.ping()
Test.statistics()

print("finish")