import logging
import os
import sys
from CosmicKSP import settings


format = "%(asctime)s | %(levelname)-8s | %(message)s"


class ColoredFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey,
        logging.INFO: grey,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_fmt = f'%(asctime)s | {self.FORMATS.get(record.levelno)}%(levelname)-8s{self.reset} | %(filename)s:Line %(lineno)s | %(message)s'
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging_level = settings.LOGGING_LEVEL

logger = logging.getLogger('CosmicKSP')
logger.setLevel(logging_level)

console_formatter = ColoredFormatter(fmt=format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging_level)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

if sys.argv[0]: # don't log to file in the python console

    if getattr(sys, 'frozen', False):
        app_name = os.path.basename(os.path.abspath(sys.argv[0]))
    else:
        app_name = os.path.basename(os.path.dirname(os.path.abspath(sys.argv[0])))

    app_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    file_formatter = logging.Formatter(fmt=format)

    log_file = os.path.join(app_path, f'{app_name}.log')
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
