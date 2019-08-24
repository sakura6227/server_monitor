import logging
import logging.handlers

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class Loger(Singleton):
    def __init__(self, logFilePath = './Monitor'):
        # get the logger
        self.logger = logging.getLogger()
        self.logfileName = logFilePath
        self.logformattor = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        # self.logSplitHandle = logging.handlers.TimedRotatingFileHandler(self.logfileName, when='M', interval=0, backupCount=40)
        # self.logSplitHandle.suffix = "_%Y%m%d.log"

        # add formattor to the logger
        self.logHandle = logging.FileHandler(self.logfileName)
        self.logHandle.setFormatter(self.logformattor)
        self.logger.addHandler(self.logHandle)
        self.logger.setLevel(logging.NOTSET)
        # self.logger.addHandler(self.logSplitHandle)

    # log the info
    def log_Info(self, log_info):
        self.logger.info(log_info)

    # log the error
    def log_Error(self, log_error):
        self.logger.error(log_error)

    # log the debug
    def log_Debug(self, log_debug):
        self.logger.debug(log_debug)
