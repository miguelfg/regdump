# -*- coding: utf-8 -*-
from fabric.api import env

__author__ = 'miguelfg'


###########
# ENVIRONMENTS
###########
prod_roles = {
    'test': ['localhost'],
    'dev': ['localhost'],
    'prod': ['ubuntu@scraper-1']
}
