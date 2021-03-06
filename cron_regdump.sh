#! /bin/bash
cd /home/miguelfg/workspace/python_environments/prometheus-panadata3
source bin/activate

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

export PANADATA_DB='sqlite:////home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/data/panama_registry.db'
export PANADATA_SLEEP_SECS=0.3
export PANADATA_FILES_DIR='/media/big_HD/workspace/projects/prometheus/src/panadata/data/htmls/'
#export WORKON_HOME=~/.virtualenvs/
#source /usr/local/bin/virtualenvwrapper.sh
#workon prometheus_panadata3
python /home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/regdump.py --size 10
