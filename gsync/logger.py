import logging
from typing import TextIO

__all__ = ["get_logger"]

LOG_LEVEL = {"debug": logging.DEBUG,
             "info": logging.INFO,
             "warning": logging.WARNING,
             "error": logging.ERROR,
             "critical": logging.CRITICAL}


def get_logger(name: str = None, stdout_filter_level: str = "info"):
    name = __name__ if name is None else name
    logger = logging.getLogger(name=name)
    formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler()
    if stdout_filter_level not in LOG_LEVEL.keys():
        raise ValueError(f"{stdout_filter_level} is not a correct log level! ({LOG_LEVEL.keys()})")
    stdout_filter_level = LOG_LEVEL[stdout_filter_level]

    ch.setLevel(stdout_filter_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(stdout_filter_level)

    return logger
