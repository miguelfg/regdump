#!/bin/bash
### THIS COMMAND LINE WORKS!! AND SUBSTITUTES ALL THE FOLLOWING
$ for i in 1 2; do ssh -A scraper-$i "screen -dmS scraper && source /usr/local/bin/virtualenvwrapper.sh && workon prometheus_panadata34 && pwd" ; done
$ for i in 1 2; do ssh -A scraper-$i "screen -dmS scraper && source /usr/local/bin/virtualenvwrapper.sh && workon prometheus_panadata34 && python regdump.py --start 21654$i --stop 900000 --step 10" ; done
$ for i in 1 2; do ssh -A scraper-$i "ps -A | grep python" ; done

### DON'T RUN THIS FILE, IS JUST INFORMATIVE
#hostname
#export WORKON_HOME=~/.virtualenvs/
#source /usr/local/bin/virtualenvwrapper.sh
#workon prometheus_panadata34
#pwd
#id=${HOSTNAME//[a-zA-Z\-]/}
#sleep 10 &
##python reg_dump --start 216541 --stop 900000 --step $id &
#
