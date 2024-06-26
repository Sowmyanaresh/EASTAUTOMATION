import logging
class LogGen():
    @staticmethod
    def loggen():
        logger = logging.getLogger()
        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            handler  = logging.FileHandler(".\\Logs\\testlog.log", 'a', 'utf-8')
            formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s') # or whatever
            handler.setFormatter(formatter) # Pass handler as a parameter, not assign
            logger.addHandler(handler)
        return logger