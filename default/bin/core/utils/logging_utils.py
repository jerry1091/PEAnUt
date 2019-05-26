import logging

from core.config import log_path, app_name, log_format


def setup_logger(name, log_file, formatter, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Main app log
app_log_file = '{}{}.log'.format(log_path, app_name)
app_logger = setup_logger('app_logger', app_log_file, log_format)

# api log
api_log_file = '{}{}_api.log'.format(log_path, app_name)
api_logger = setup_logger('api_logger', api_log_file, log_format)
