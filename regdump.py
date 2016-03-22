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
    parser.add_argument('--query', dest='query', type=str)
    parser.add_argument('--start', dest='start', type=int, default=None)
    parser.add_argument('--stop', dest='stop', type=int, default=None)
    parser.add_argument('--size', dest='size', type=int, default=100)
    parser.add_argument('--step', dest='step', type=int, default=1)
    args = parser.parse_args()

    logger.info('regdump started')

    if args.query:
        logger.info('performing query: %s', str(args.query))
        sociedades = crawler.query(args.query)
    else:
        if not args.start:
            # get last index of record in database
            # sociedades_ids = crawler.old_fichas
            # print(len(sociedades_ids))
            # print(max(sociedades_ids))
            # max_id = max(sociedades_ids)
            # args.start = max_id
            args.start = db_worker.find_max_ficha() + 1
            logger.info('found %i sociedades already in DB', args.start)

        if not args.stop:
            args.stop = args.start + args.size

        logger.info('it will scrape from %i to %i', args.start, args.stop)
        sociedades = crawler.brute_sociedades(args.start, args.stop, args.step)


    logger.info('found %i sociedades', len(sociedades))
    logger.info('found %i personas',
                len([item for sublist in [sociedad.personas for sociedad in sociedades] for item in sublist]))
    logger.info('regdump finished')
