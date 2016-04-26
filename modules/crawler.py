import os
from Classes import *

from modules import parser, db_worker
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep
from datetime import datetime
from random import sample
import urllib.request

from modules.helper import get_logger
logger = get_logger('crawler')

SLEEP_SECS = float(os.getenv('PANADATA_SLEEP_SECS', 4))
FILES_DIR = os.getenv('PANADATA_FILES_DIR', None)

user_agents = [
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/3.1',
    'Opera/7.51 (Windows NT 5.1; U)',
]
old_fichas = db_worker.get_fichas()


def query_url(page, query):
    return (
        'http://201.224.39.199/scripts/nwwisapi.dll/conweb/MESAMENU?TODO=MER4&START=%s&FROM=%s' % (str(page), query))


def ficha_url(ficha):
    return ('http://201.224.39.199/scripts/nwwisapi.dll/conweb/MESAMENU?TODO=SHOW&ID=%s' % str(ficha))


def brute_sociedades(start,stop,step):
    fichas = range(start, stop, step)
    queue=[]
    for ficha in fichas:
        if ficha not in old_fichas:
            ua = sample(user_agents, 1)[0]
            headers = {'User-Agent': ua}
            url = ficha_url(ficha)
            req = urllib.request.Request(url, headers=headers)
            # req.add_header('Referer', ua)
            # req.add_header('User-Agent', ua)
            from urllib.error import URLError, HTTPError
            try:
                # response = urlopen(req)
                resp = urllib.request.urlopen(req)
            except HTTPError as e:
                logger.error('HTTP Error code: ', e.code)
            except URLError as e:
                logger.error('URL Error Reason: ', e.reason)
            else:
            # with urllib.request.urlopen(req) as r:
            #     logger.info('response to %i returned status'.format(i, resp.), len(queue))
                ts = datetime.now().strftime("%Y-%m-%d_%I-%M-%S")
                html = resp.read()
                html = html.decode('ISO-8859-1', 'ignore')
                if FILES_DIR and os.path.exists(FILES_DIR) and os.path.isdir(FILES_DIR):
                    with open("{}{}sociedad_{}_on_{}.html".format(FILES_DIR, os.sep, ficha, ts), mode='w') as of:
                        of.write(html)
                sociedad = parse_sociedad_html(html)
                queue.append(sociedad)
                sleep(SLEEP_SECS)

    logger.info('found %i sociedades', len(queue))

    return queue


def parse_sociedad_html(html):
    if parser.exists(html):
        soup = BeautifulSoup(html, 'html.parser', parse_only=SoupStrainer('p'))
        sociedad = scrape_sociedad_data(soup)
        if sociedad:
            logger.info('found sociedad %s', sociedad.nombre)
            personas, asociaciones = scrape_personas(soup)
            logger.debug('found %i personas', len(personas))
            logger.debug('found %i asociaciones', len(asociaciones))
            return db_worker.resolve_sociedad(sociedad, personas, asociaciones)
        else:
            logger.warn("Error with html: {}".format(html))

    return None


def scrape_personas(soup):
    directores = scrape_sociedad_directores(soup)
    subscriptores = scrape_sociedad_subscriptores(soup)
    dignatarios = scrape_sociedad_dignatarios(soup)
    personas = set().union(*[directores, unpack_personas_in_dignatarios(dignatarios), subscriptores])
    asociaciones = dict(
        list({'directores': directores, 'subscriptores': subscriptores}.items()) + list(dignatarios.items()))
    return [personas, asociaciones]


def scrape_sociedad_directores(soup):
    try:
        directores = {Persona(persona) for persona in parser.collect_directores(soup)}
    except Exception as e:
        print(e)
        logger.exception("Error scraping directors on soup: {}".format(soup.prettify()))
        return set()
    return directores


def scrape_sociedad_subscriptores(soup):
    try:
        subscriptores = {Persona(persona) for persona in parser.collect_subscriptores(soup)}
    except Exception as e:
        print(e)
        logger.exception("Error scraping subscriptores on soup: {}".format(soup.prettify()))
        return {}
    return subscriptores


def scrape_sociedad_dignatarios(soup):
    try:
        dignatarios = {item[0]: {Persona(value) for value in item[1]} for item in
                       parser.collect_dignatarios(soup).items()}
    except Exception as e:
        print(e)
        logger.exception("Error scraping dignatarios on soup: {}".format(soup.prettify()))
        return {}
    return dignatarios


def unpack_personas_in_dignatarios(dignatarios):
    return {val for sublist in dignatarios.values() for val in sublist}


def scrape_sociedad_data(soup):
    try:
        sociedad = Sociedad(parser.collect_nombre_sociedad(soup), parser.collect_ficha(soup))
    except:
        logger.exception('Error parsing sociedad or ficha from soup {}'.format(soup.prettify()))
        return None

    sociedad.fecha_registro = parser.collect_fecha_registro(soup)
    sociedad.provincia = parser.collect_provincia(soup)
    sociedad.notaria = parser.collect_notaria(soup)
    sociedad.duracion = parser.collect_duracion(soup)
    sociedad.status = parser.collect_status(soup)
    sociedad.agente = parser.collect_agente(soup)
    sociedad.moneda = parser.collect_moneda(soup)
    sociedad.capital = parser.collect_capital(soup)
    sociedad.capital_text = parser.collect_capital_text(soup)
    sociedad.representante_text = parser.collect_representante_text(soup)
    return sociedad
