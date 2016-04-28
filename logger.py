class Logger(object):
    """ Implementation of a Logger using the Borg pattern """

    __shared_state = {'level':'DEBUG'}
    def __init__(self, level):
        self.__shared_state['level'] = level
        self.__dict__ = self.__shared_state

    def log(self, message):
        print message

logger = Logger('INFO')
