_author_ = 'Srikrishna'

'''
    Simple socket server
'''
import HttpService

import socket
import sys
import thread
import logging
logger = logging.getLogger(__name__)
import json
import re

SENS = {
    "ENERGY":{
        "D0":"4",
        "D1":"voltage",
        "D2":"current",
        "D3":"frequency",
        "D4":"power_factor",
        "D5":"active_power",
        "D6":"reactive_power",
        "D7":"apparent_power",
        "D8":"active_energy",
        "D9":"reactive_energy"
    },
    "WATER":{
        "D0":"2",
        "D1":"water_level",
        "D2":"water_temperature"
    },
    "POLLUTION":{
        "D0":"5",
        "D1":"128",
        "D2":"256",
        "D3":"512",
        "D4":"1024",
        "D5":"2048",
        "D6":"4096"
    }
}

class SocketServer(object):
    def __init__(self, port):
        self.BUFF = 256
        self.HOST = ''  # Symbolic name, meaning all available interfaces
        self.PORT = int(port)  # Arbitrary non-privileged port
        self.http = HttpService.HTTP_Request()
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logger.info("Connected to %s ", self.connection)
        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('Initialzation Failed')

    def cleanData(self, data):
        try:
            cdata = re.search('({.+?})', data)
            if cdata:
                data_parse = json.loads(cdata.groups(1)[0])

                sen_values = SENS[data_parse['type']]["D0"]
                count = 1
                while count <= int(sen_values):
                    str_sen = "D"+str(count)
                    print str_sen
                    data_json = {"observations": [{
                        "value": data_parse[str_sen]}
                    ]}
                    print data_json
                    count = count+1
                    self.http.putRequest(SENS[data_parse['type']][str_sen], data_json)

                for val in data_parse:
                    print(val)

            else:
                logger.info("Data cannot be parsed")




        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('Data cleaning failed')


    def handler(self,clientsock, addr):
        try:
            while 1:
                data = clientsock.recv(int(self.BUFF))
                logger.info('Received data:' + repr(data))
                self.cleanData(data)
                break
        except Exception, e:
            logging.error(e, exc_info=True)

    def connect(self):

        try:
            self.connection.bind((self.HOST, self.PORT))
        except socket.error as msg:
            logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        logger.info('Socket bind complete')

        try:
            self.connection.listen(10)
            while 1:
                #wait to accept a connection - blocking call
                conn, addr = self.connection.accept()
                logger.info('Connected with ' + addr[0] + ':' + str(addr[1]))

                thread.start_new_thread(self.handler, (conn, addr))

        except Exception, e:
            logging.error(e, exc_info=True)
            logger.error('Connection Failed')

        finally:
            # Clean up the connection
            conn.close()

    def disconnect(self):
        self.connection.close()
