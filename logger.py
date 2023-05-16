import logging
import time


class MyFormatter(logging.Formatter):
    formats = {
        logging.DEBUG: "%(module)s: %(lineno)d: %(msg)s",
        logging.INFO: "%(asctime)s - %(levelname)s - %(message)s",
        logging.WARNING: "%(asctime)s - %(levelname)s - %(message)s",
        logging.ERROR: "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s",
    }

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        super().__init__(fmt)

    def format(self, record):
        # Get the format based on the logging level
        log_fmt = self.formats.get(record.levelno, self._fmt)

        # Call the original formatter class to do the grunt work
        result = logging.Formatter(log_fmt).format(record)

        return result


def initialize_logger(name):
    starttime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    logger = logging.getLogger(name)

    fmt = MyFormatter()

    # hdlr = logging.FileHandler(f"Logs/{starttime}.log", mode="w")
    hdlr = logging.FileHandler(f"Logs/{'APP'}.log", mode="w")
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(fmt)

    ch = logging.StreamHandler()  # Dodanie StreamHandlera dla logów konsolowych
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    # TODO Add SMPThandler to init e-mail sandler for errors

    logger.addHandler(hdlr)
    logger.addHandler(ch)  # Dodanie StreamHandlera do loggera

    logger.setLevel(logging.DEBUG)
    # logger.propagate = True  ## wyłącza logowanie w konsoli
    return logger


def get_logger(name):
    logger = initialize_logger(name)
    return logger
