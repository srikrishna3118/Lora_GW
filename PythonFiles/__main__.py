import RF_TestBed

import sys
import glob
import logging
import logging.handlers


LOG_FILE = "syslog_GW.log"
logging.basicConfig(format='%(asctime)s %(message)s',filename=LOG_FILE,level=logging.DEBUG)



logging.info('Main:Started')

Test = RF_TestBed.RF_TestBed()

try:
    Test.Test()
    Test.setValues(10,5)
except Exception, e:
    logging.error(e, exc_info=True)
print("finish")