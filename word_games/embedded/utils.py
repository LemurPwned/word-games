import logging


def logger_config():
    logging.basicConfig(
        format='[%(process)d]%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    return logging.getLogger(__name__)
