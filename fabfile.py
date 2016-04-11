# -*- coding: utf-8 -*-
from fabric.api import *
from fab_config import prod_roles
from contextlib import contextmanager as _contextmanager

__author__ = 'miguelfg'


###########
# CONFIG
###########
env.roledefs = {
    'test': ['localhost'],
    'dev': ['localhost'],
}
env.roledefs.update(prod_roles)

env.use_ssh_config = True
env.venvs_root = '~/.virtualenvs/'
env.venv_name = 'prometheus_panadata34'
env.activate = 'source {}{}/bin/activate'.format(env.venvs_root, env.venv_name)

PROJECT_DIR = '/var/www/prometheus_panadata'

###########
# COMMANDS
###########
@task
@parallel
def basic_setup():
    """
    """
    apt_install('build-essential')
    apt_install('python-dev')
    apt_install('python-setuptools')
    apt_install('git')
    easy_install('pip')
    virtualenv_setup()


@task
@parallel
def virtualenv_setup():
    apt_install('virtualenv python-virtualenv')
    pip_install('virtualenvwrapper')
    run("echo 'export WORKON_HOME={}' >> ~/.bashrc".format(env.venvs_root))
    run("echo 'mkdir -p $WORKON_HOME' >> ~/.bashrc")
    run("echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc")


@_contextmanager
def virtualenv():
    with prefix(env.activate):
        yield


@task
@parallel
def virtualenv_create():
    with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
        run("mkvirtualenv --python=/usr/bin/python3.4 " + env.venv_name)
        with cd(PROJECT_DIR):
            run("setvirtualenvproject")


@task
def pip_freeze():
    with virtualenv():
        run("pip freeze")


@task
def install_repo(root='/var/www/', folder_name='prometheus_panadata'):
    """
    Clones the repo into a local directory
    """
    with settings(warn_only=True):
        run('sudo mkdir -p {}'.format(root))
        with cd(root):
            run('sudo git clone https://github.com/miguelfg/regdump ' + folder_name)


@task
@parallel
def install_server():
    """
    """
    # install basic stuff
    basic_setup()

    # set up repo
    install_repo()

    # create virtualenv
    virtualenv_create()

    # set up DB connection

    # install requirements
    with cd(PROJECT_DIR):
        with virtualenv():
            pip_install('-r requirements.txt')

        # set permission and ownership to user!


@task
def host_type():
    run('uname -a')


###########
# UTILITIES
###########
def apt_install(package):
    """
    Install a single package on the remote server with Apt.
    """
    sudo('aptitude install -y %s' % package)


def easy_install(package):
    """
    Install a single package on the remote server with easy_install.
    """
    sudo('easy_install %s' % package)


def pip_install(package):
    """
    Install a single package on the remote server with pip.
    """
    sudo('pip install %s' % package)


def with_virtualenv(command):
    """
    Executes a command in this project's virtual environment.
    """
    run('source bin/activate && %s' % command)
