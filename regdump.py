#!/usr/bin/python3
import argparse
import logging.config
import os

import yaml

from modules import crawler
from modules import parser, db_worker

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# create logger
logging.config.dictConfig(yaml.load(open('logging.yaml', 'r').read()))
logger = logging.getLogger('regdump')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query registro-publico.gob.pa for sociedades.')
    parser.add_argument('--start', dest='start', type=int, default=None)
    parser.add_argument('--stop', dest='stop', type=int, default=None)
    parser.add_argument('--size', dest='size', type=int, default=100)
    parser.add_argument('--step', dest='step', type=int, default=1)
    args = parser.parse_args()

    logger.info('regdump started')

    if args.start is None:
        args.start = db_worker.find_max_ficha()
        logger.info('found %i sociedades already in DB', args.start)

    if not args.stop:
        args.stop = args.start + args.size

    # always add 1, as it's meant to stop at given id and not before
    args.stop += 1

    logger.info('it will scrape from %i to %i with steps of %i', args.start, args.stop, args.step)
    sociedades = crawler.brute_sociedades(args.start, args.stop, args.step)
    logger.info('regdump finished')
