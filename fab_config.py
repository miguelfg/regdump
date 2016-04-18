# -*- coding: utf-8 -*-
from fabric.api import env

__author__ = 'miguelfg'

###########
# CONFIG
###########

REPO_URL = 'git@github.com:miguelfg/regdump.git'
PROJECT_FOLDER_NAME = 'prometheus_panadata'
PROJECTS_ROOT = '/var/www/'
PROJECT_DIR = PROJECTS_ROOT + PROJECT_FOLDER_NAME

env.venvs_root = '~/.virtualenvs/'
env.venv_name = 'prometheus_panadata34'
env.activate = 'source {}{}/bin/activate'.format(env.venvs_root, env.venv_name)

env.roledefs = {}
prod_roles = {
    'test': ['localhost'],
    'dev': ['localhost'],
    'prod': ['mfiandor@scraper-1']
}
env.roledefs.update(prod_roles)

env.use_ssh_config = True
# env.key_filename = '~/.ssh/id_rsa'
# env.forward_agent = True
