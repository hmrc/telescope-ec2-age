import logging
import sys
from logging import Logger


def get_logger(level: int = logging.INFO) -> Logger:
    logger: Logger = logging.getLogger('telescope-ec2-age')
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
