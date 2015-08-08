import logging


class Logger(object):
    logger = None
    handler = None

    def __init__(self, level_=10):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=level_)

        self.handler = logging.FileHandler('e2c2.log')
        self.handler.setLevel(level=level_)

        fmt = "[%(asctime)s %(levelname)s] %(name)s:%(module)s -> line %(lineno)d - %(message)s"
        self.handler.setFormatter(logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S"))

        self.logger.addHandler(self.handler)