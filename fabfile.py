# -*- coding: utf-8 -*-
from fabric.api import *
from fab_config import prod_roles

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


###########
# COMMANDS
###########
@task
@parallel
def basic_setup():
    apt_install('build-essential')
    apt_install('python-dev')
    apt_install('python-setuptools')
    apt_install('python-virtualenv')
    apt_install('git')
    easy_install('pip')


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
    # install basic stuff
    basic_setup()

    # set up repo
    install_repo()

    # set up DB connection

    # install requirements
    with cd(env.user_home):
        with_virtualenv(pip_install('-r requirements.txt'))

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
