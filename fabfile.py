# -*- coding: utf-8 -*-
import os
import time

from fabric.colors import *
from fabric.api import task, parallel, run, prefix, cd, sudo, settings
from fab_config import prod_roles, env
from fab_config import PROJECTS_ROOT, PROJECT_DIR, REPO_URL, PROJECT_FOLDER_NAME
from contextlib import contextmanager as _contextmanager

__author__ = 'miguelfg'


###########
# COMMANDS
###########
@task
def basic_setup():
    """
    """
    apt_install('build-essential')
    apt_install('python-dev')
    apt_install('python-setuptools')
    apt_install('libyaml-dev libpython2.7-dev')
    apt_install('git')
    easy_install('pip')
    virtualenv_setup()


@task
@parallel
def virtualenv_setup():
    """
    Install virtualenv, virtualenvwrapper, and configs them
    """
    apt_install('virtualenv python-virtualenv')
    pip_install('virtualenvwrapper', globally=True)
    run("echo 'export WORKON_HOME={}' >> ~/.bashrc".format(env.venvs_root))
    run("echo 'mkdir -p $WORKON_HOME' >> ~/.bashrc")
    run("echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc")


@task
def virtualenv_add_to_postactivate(line):
    """
    Add a line to the postactivate script of current virtualenv
    """
    with cd(env.venvs_root):
        run("echo '' >> {}/bin/postactivate".format(env.venv_name))
        run("echo '{}' >> {}/bin/postactivate".format(line, env.venv_name))
        run("echo '' >> {}/bin/postactivate".format(env.venv_name))


@task
@parallel
def virtualenv_create(python='python2.7'):
    """
    Creates a new virtualenv and sets the project directory of virtualenvwrapper variable
    """
    with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
        run("mkvirtualenv --python=/usr/bin/{} {}".format(python, env.venv_name))
        with cd(PROJECT_DIR):
            run("setvirtualenvproject")


@task
@parallel
def virtualenv_check_python_version():
    """
    Check python version installed in current virutalenv
    """
    with virtualenv():
        run("python -V")


@task
def echo_venv(something):
    with virtualenv():
        run('echo $%s' % something)


@task
def pip_freeze():
    """
    Prints external libs installed in project's virtualenv
    """
    with virtualenv():
        run("pip freeze")


@task
def ll(dir=PROJECTS_ROOT):
    """
    List the given directory
    """
    run('ls -l {}'.format(dir))


@task
def add_sudoer(username):
    """
    Adds a user as sudoer
    """
    run('sudo adduser {} sudo'.format(username))


@task
def delete_repo(root=PROJECTS_ROOT, folder_name=PROJECT_FOLDER_NAME):
    """
    Removes the installed repo in the given directory
    """
    with cd(root):
        run('sudo rm -rf {}'.format(folder_name))


@task
def install_repo(repo_url=REPO_URL, root=PROJECTS_ROOT, folder_name=PROJECT_FOLDER_NAME):
    """
    Clones the repo into a local directory
    """
    with cd('/tmp'):
        run('git clone ' + repo_url + ' ' + folder_name)

    with cd(root):
        run('sudo mv /tmp/{} .'.format(folder_name))

    project_dir = root + folder_name if root.endswith(os.sep) else root + os.sep + folder_name
    with cd(project_dir):
        run('mkdir data/')
        run('mkdir logs/')


@task
def install_requirements(req_file='-r requirements.txt', upgrade=' --upgrade '):
    with virtualenv():
        with cd(PROJECT_DIR):
            # run('pip install ' + upgrade + req_file)
            pip_install(upgrade + req_file)


@task
@parallel
def install_server():
    """
    """
    # set server's hostname
    set_host_name()

    # install basic stuff
    basic_setup()

    # set up repo
    install_repo()

    # create virtualenv
    virtualenv_create()

    # TODO: set up DB connection

    # install requirements
    with cd(PROJECT_DIR):
        with virtualenv():
            pip_install('-r requirements.txt')

        # TODO: set permission and ownership to user!
        # TODO: set db env variable


@task
def push_repo(repo_dir=PROJECT_DIR, message=None, branch='master'):
    """
    Runs git push on server's project directory
    """
    with cd(repo_dir):
        run('git add .')
        if not message:
            message = 'pushed changes automatically on {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
        run('git commit -m "{}"'.format(message))
        run('git push origin {}'.format(branch))


@task
def pull_repo(repo_dir=PROJECT_DIR):
    """
    Runs git pull on server's project directory
    """
    with cd(repo_dir):
        run('git pull')


@task
def reg_dump(start=None, stop=None, size=None, step=None):
    """
    The real scraper process.
    :param start:
    :param stop:
    :param size:
    :param step:
    :return:
    It's meant to be executed like:
    python reg_dump --start 200000 --stop 1000000 --step <<server hostname id>>
    python reg_dump --start 200000 --stop 1000000 --step hostname_id
    python reg_dump --start 216543 --stop 1000000 --step hostname_id
    """
    with virtualenv():
        with cd(PROJECT_DIR):
            args = ''
            if start:
                args += ' --start=' + start
            if stop:
                args += ' --stop=' + stop
            if size:
                args += ' --size=' + size
            if step:
                if step == 'hostname_id':
                    import socket
                    step = str(socket.gethostname()).rsplit('-', 1)[1]
                args += ' --step=' + step
            run('python regdump.py' + args)


@task
def max_sociedades():
    """
    """
    with virtualenv():
        with cd(PROJECT_DIR):
            run('python max_sociedades.py')


@task
def tail_history(lines=20):
    """
    Tails the history log
    """
    with virtualenv():
        with cd(PROJECT_DIR):
            run('tail -n {} history.log'.format(lines))


@task
def truncate_db():
    """
    Truncates all the data of the db
    """
    pass


# def TODO: reg_dump_test():
# def TODO: reg_dump_check_history_log():
# def TODO: reg_dump_check_db_records():


@task
def host_type():
    run('uname -a')


@task
def set_host_name(host=None):
    hostname = host if host else env.host_string
    if '@' in hostname:
        hostname = hostname.rsplit('@')[1]
    if ':' in hostname:
        hostname = hostname.split(':')[0]
    sudo('echo "{}" > /etc/hostname'.format(hostname))
    sudo('service hostname restart')


###########
# UTILITIES
###########
@task
def apt_install(package):
    """
    Install a single package on the remote server with Apt.
    """
    sudo('aptitude install -y %s' % package)


@task
def easy_install(package):
    """
    Install a single package on the remote server with easy_install.
    """
    sudo('easy_install %s' % package)


@task
def pip_install(package, globally=False):
    """
    Install a single package on the remote server with pip.
    """
    if globally:
        sudo('pip install %s' % package)
    else:
        with virtualenv():
            run('pip install %s' % package)


@_contextmanager
def virtualenv():
    """
    Context manager to run commands under an activated virtualenv
    """
    # with prefix(env.activate):
    with prefix('WORKON_HOME=%s' % env.venvs_root):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            with prefix('workon %s' % env.venv_name):
                yield

