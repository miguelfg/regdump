#! /bin/bash
#TODO: THIS IS NOT WORKING - THAT'S WHY WE EXPORT THE DB ENV VARIABLE BELOW
cd /home/miguelfg/workspace/python_environments/prometheus-panadata35
source bin/activate

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

export PANADATA_DB='sqlite:////home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/data/panama_registry.db'
echo $PANADATA_DB
python /home/miguelfg/workspace/projects/apache_solr/prometheus/src/panadata_regdump/regdump.py --start 20000 --size 3
#cdproject && python regdump.py --size 1
