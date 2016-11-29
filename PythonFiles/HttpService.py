_author_ = 'Srikrishna'

import requests
import json
import random
import httplib

import logging
logger = logging.getLogger(__name__)

#agent = Agent(reactor)




class HTTP_Request:
    def __init__(self):
        self.Response = ''
        self.token = 'e6c55c5a809e07e563996c144382b9606aca417c25f54b0f7e1bb8360dc75b0a'
        #self.token = '646967a9f99ae76cfb836026d0015c4b80f8c0e1efbd3d261250156efd8fb96f'

    def getData(self):
        value = random.randint(1, 99)
        return str(value)

    def putRequest(self, stream_id, data_packet):
        header = {'content-type': 'application/json', 'IDENTITY_KEY': self.token}

        try:
            url = 'http://rbccps.ddns.net:8081/data/RBCCPS/'
            url = url + stream_id + "/"
            logger.info("sending data to")
            logger.info(url)
            #data = json.dumps(data_packet)

            #Call REST API
            response = requests.put(url, headers=header, data=json.dumps(data_packet))
            logger.info(response.text)

        except Exception, e:
            logging.error(e, exc_info=True)




