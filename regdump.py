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


def log_scraped(sociedades):
    # logger.info('found %s sociedades', type(sociedades))
    logger.info('found %i sociedades', len(sociedades))
    logger.info('found %i personas',
                len([item for sublist in [sociedad.personas for sociedad in sociedades] for item in sublist]))


if __name__ == "__main__":
    """
    query: it is the 'FROM' parameter at the scraping URL:
        'http://201.224.39.199/scripts/nwwisapi.dll/conweb/MESAMENU?TODO=MER4&START=%s&FROM=%s' % (str(page), query))
    start: index number to start scraping
    stop: index number to stop scraping
    size: if 'stop' is not provided, this is add to 'start' to calculate the numbers of records/fichas to scrape
    step: is the size of the jump from one record to scrape to the next one, usually 1
    """
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
        log_scraped(sociedades)
    else:
        if not args.start:
            # get last index of record in database
            # sociedades_ids = crawler.old_fichas
            # print(len(sociedades_ids))
            # print(max(sociedades_ids))
            # max_id = max(sociedades_ids)
            # args.start = max_id
            max_ficha = db_worker.find_max_ficha()
            logger.info('found %i sociedades already in DB', max_ficha)
            args.start = max_ficha + 1

        if not args.stop:
            args.stop = args.start + args.size

        if args.start >= args.stop:
            logger.warn('Not scraping anything, your stop parameter(%i) is lower than start parameter(%i)', args.stop, args.start)
        else:
            logger.info('it will scrape from %i to %i', args.start, args.stop)
            sociedades = crawler.brute_sociedades(args.start, args.stop, args.step)
            log_scraped(sociedades)

    logger.info('regdump finished')
