
from FishHunterUtil.colargulog import ColorizedArgsFormatter, BraceFormatStyleFormatter
import logging
import sys

def init_logging(log_file="", list_disable_logger=["requests"]):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for logger_name in list_disable_logger:
        logging.getLogger(logger_name).propagate = False

    console_level = "INFO"
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(console_level)
    console_format = "%(asctime)s :: %(levelname)-4s :: %(message)s"
    colored_formatter = ColorizedArgsFormatter(console_format)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)

    if log_file != "":
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8", delay=False)
        file_level = "DEBUG"
        file_handler.setLevel(file_level)
        file_format = "%(asctime)s - %(name)s (%(lineno)s) - %(levelname)-8s - %(threadName)-12s - %(message)s"
        file_handler.setFormatter(BraceFormatStyleFormatter(file_format))
        root_logger.addHandler(file_handler)

    # ignore encoding error
    logging.captureWarnings(True)