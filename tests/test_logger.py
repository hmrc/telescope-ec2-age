import logging
from telemetry.telescope_ec2_age.logger import get_logger


def test_logger():
    logger = get_logger(logging.CRITICAL)
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.CRITICAL
