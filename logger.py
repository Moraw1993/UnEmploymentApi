import logging
from logging import handlers
import time
import os


class MyFormatter(logging.Formatter):
    """
    Custom log formatter class.

    Formats log records based on the logging level.

    Attributes:
        formats (dict): Dictionary mapping logging levels to format strings.

    """

    formats = {
        logging.DEBUG: "%(module)s: %(lineno)d: %(msg)s",
        logging.INFO: "%(asctime)s - %(levelname)s - %(message)s",
        logging.WARNING: "%(asctime)s - %(levelname)s - %(message)s",
        logging.ERROR: "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s",
    }

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        super().__init__(fmt)

    def format(self, record):
        """
        Formats the log record based on the logging level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.

        """

        # Get the format based on the logging level
        log_fmt = self.formats.get(record.levelno, self._fmt)

        # Call the original formatter class to do the grunt work
        result = logging.Formatter(log_fmt).format(record)

        return result


def initialize_logger(name):
    """
    Initializes and configures a logger with file and console handlers.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger.

    """

    starttime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    logger = logging.getLogger(name)

    fmt = MyFormatter()

    # Configure the file handler for writing logs to a file
    hdlr = logging.FileHandler(f"Logs/{starttime}.log", mode="w")
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(fmt)

    # Configure the console handler for printing logs to the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    # TODO: Add SMTPHandler to initialize email handler for error logging
    ## Smtplogger
    email_subject = f"Error occurred in UnEmploymentApi Download. Look at log {starttime}.log"  ## temporary
    host = os.getenv("mailhost")
    port = os.getenv("port")
    emailFrom = os.getenv("EmailAcc")
    emailTo: list = os.getenv("EmailTo").split(",")
    credentials: tuple = (os.getenv("EmailAcc"), os.getenv("EmailPass"))

    smtp_handler = handlers.SMTPHandler(
        mailhost=(host, port),
        fromaddr=emailFrom,
        toaddrs=emailTo,
        subject=email_subject,
        credentials=credentials,
        secure=(),
    )
    smtp_handler.setLevel(logging.ERROR)
    smtp_handler.setFormatter(fmt)

    # Add the handlers to the logger
    logger.addHandler(smtp_handler)
    logger.addHandler(hdlr)
    logger.addHandler(ch)

    logger.setLevel(logging.DEBUG)
    # logger.propagate = True  ## wyłącza logowanie w konsoli

    return logger


def get_logger(name):
    """
    Retrieves the initialized logger.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger.

    """
    logger = initialize_logger(name)
    return logger
