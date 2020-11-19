import logging
from telemetry.telescope_ec2_age.logger import create_app_logger


def test_logger():
    logger = create_app_logger(logging.CRITICAL)
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.CRITICAL
