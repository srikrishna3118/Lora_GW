_author_ = 'Srikrishna'

import ConfigParser

sections = 'Connection','Configuration','Testing'

class MyConfiguration(object):

    def __init__(self, *file_names):
        parser = ConfigParser.ConfigParser()
        parser.optionxform = str  # make option names case sensitive
        found = parser.read(file_names)
        if not found:
            raise ValueError('No config file found!')
        for names in sections:
            self.__dict__.update(parser.items(names))



#config = MyConfiguration('lora.conf')    # define the configurations in this file

