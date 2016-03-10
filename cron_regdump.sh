#! /bin/bash
cd /home/miguelfg/workspace/python_environments/prometheus-panadata3
source bin/activate

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

export panadata_db='sqlite:////home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/data/panama_registry.db'
python /home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/regdump.py --size 10
#cdproject && python regdump.py --size 1
