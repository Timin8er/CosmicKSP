"""logger for the Cosmic KSP project"""
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import faulthandler
from typing import Dict

faulthandler.enable()

DEFAULT_FORMAT: str = "  | %(levelname)-8s %(asctime)s | %(message)s"
FILE_FORMAT: str = "  | %(levelname)-8s %(asctime)s | %(message)s"
DEFAULT_LOG_DIR = os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP'))

class ColoredFormatter(logging.Formatter):
    """adds colors reflecting the siverity of the log message"""

    # grey = "\x1b[38;20m"
    # cyan = "\x1b[96;20m"
    # yellow = "\x1b[33;20m"
    # red = "\x1b[31;20m"
    # bold_red = "\x1b[31;1m"
    # reset = "\x1b[0m"

    FORMATS: Dict = {
        logging.NOTSET:    logging.Formatter(DEFAULT_FORMAT),
        logging.DEBUG:     logging.Formatter('  | \033[96;20m%(levelname)-8s\x1b[0m %(asctime)s | %(filename)s \
            , Line %(lineno)s \n    %(message)s'),
        logging.INFO:      logging.Formatter(DEFAULT_FORMAT),
        logging.WARNING:   logging.Formatter('  | \x1b[33;20m%(levelname)-8s\x1b[0m %(asctime)s | %(message)s'),
        logging.ERROR:     logging.Formatter('  | \x1b[31;20m%(levelname)-8s\x1b[0m %(asctime)s | %(message)s'),
        logging.CRITICAL:  logging.Formatter('  | \x1b[31;1m%(levelname)-8s\x1b[0m %(asctime)s | %(message)s')
    }

    def format(self, record):
        return self.FORMATS[record.levelno].format(record)


class UncoloredFormatter(logging.Formatter):
    """the formatter for files"""
    FORMATS: Dict = {
        logging.NOTSET:    logging.Formatter(DEFAULT_FORMAT),
        logging.DEBUG:     logging.Formatter('  | %(levelname)-8s | %(filename)s \
            , Line %(lineno)s \n    %(message)s'),
        logging.INFO:      logging.Formatter(DEFAULT_FORMAT),
        logging.WARNING:   logging.Formatter(DEFAULT_FORMAT),
        logging.ERROR:     logging.Formatter(DEFAULT_FORMAT),
        logging.CRITICAL:  logging.Formatter(DEFAULT_FORMAT)
    }

    def format(self, record):
        return self.FORMATS[record.levelno].format(record)


def get_logger(name: str, log_dir: str = DEFAULT_LOG_DIR, level = logging.INFO):
    """build and return a logger"""

    logger: logging.Logger = logging.getLogger(name)
    assert(not logger.hasHandlers()), 'Logger should not already have handlers'

    logger.setLevel(level)

    console_handler = logging.StreamHandler()

    if sys.platform == "win32":
        console_handler.setFormatter(UncoloredFormatter(fmt=DEFAULT_FORMAT))
    else:
        console_handler.setFormatter(ColoredFormatter(fmt=DEFAULT_FORMAT))

    logger.addHandler(console_handler)

    os.makedirs(log_dir, exist_ok=True)
    logger.LOG_FILE = os.path.join(log_dir, f'{name}.log')

    file_formatter = logging.Formatter(fmt=FILE_FORMAT)
    file_handler = RotatingFileHandler(logger.LOG_FILE, mode='a', maxBytes=1000000, backupCount=5)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # the faulthandler file io needs to be open forever
    log_file_stream = open(logger.LOG_FILE, encoding="utf-8") # pylint: disable=consider-using-with
    faulthandler.enable(file=log_file_stream)

    return logger


def tail_file(file):
    """open the log file in the terminal with the tail command"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelayDownlink"')
    else:
        os.system(f'gnome-terminal -- tail -f -n 20 {file}', shell=True)


def open_directory(dir):
    """open the log directory in your file explorer"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelayDownlink"')
    else:
        os.system(f'gio open "{dir}"')
