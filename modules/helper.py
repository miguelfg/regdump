# -*- coding: utf-8 -*-
import socket
import logging.config
import yaml

__author__ = 'miguelfg'


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


def get_logger(logger_name):
    f = ContextFilter()
    logger = logging.getLogger(logger_name)
    logging.config.dictConfig(yaml.load(open('logging.yaml', 'r').read()))
    logger.addFilter(f)
    return logger
