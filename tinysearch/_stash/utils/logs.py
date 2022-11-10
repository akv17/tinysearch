import logging


def create_logger(name, level='INFO'):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logging.basicConfig()
    return logger
