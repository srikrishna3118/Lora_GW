_author_ = 'Srikrishna'

'''
    Simple socket server
'''

import HttpService

import socket
import sys
import thread
import logging
import json
import re
import math

logger = logging.getLogger(__name__)

SENS = {
    "ENERGY":{
        "D0":"9",
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
    "ENV":{
        "D0":"5",
        "D1":"no2",
        "D2":"co2",
        "D3":"outside_temperature",
        "D4":"humidity",
        "D5":"pressure",
        "D6":"noise"
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

                sensor_type = data_parse['type'].upper()

                sen_values = SENS[sensor_type]["D0"]

                count = 1
                if(sensor_type=="WATER"):
                    logger.info("Dirty hack for now need to figure out a way to handle formulae for each sensors.")

                    V = 3.3* int(data_parse['D2'])/16384

                    R = V*10000/(3.3 - V)
                    TF = (math.log10(R/10000)/3950)+(1/298.15)
                    Temperature = (1/TF)-273.15
                    data_json = {"observations": [{
                        "value": Temperature}
                    ]}

                    self.http.putRequest(SENS[sensor_type]['D2'],data_json)
                    print data_json

                    V = 20.0457 *(math.sqrt( 273.15 + Temperature ))

                    Level = (int(data_parse['D1']) * V * 100)/400000

                    data_json = {"observations": [{
                        "value": Level}
                    ]}
                    self.http.putRequest(SENS[sensor_type]['D1'], data_json)
                    print data_json

                else:
                    while count <= int(sen_values):
                        str_sen = "D"+str(count)
                        print str_sen
                        data_json = {"observations": [{
                            "value": data_parse[str_sen]}
                        ]}
                        print data_json
                        count = count+1

                        #Http request is sent
                        self.http.putRequest(SENS[sensor_type][str_sen], data_json)

                #for val in data_parse:
                #    print(val)

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
