#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape
import configuration
from datetime import datetime  # , date, timezone
from urllib.parse import urlparse
import importlib
import os
import locale
from optparse import OptionParser, make_option

# Grab this file installation directory
INSTALLATION_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = "./templates"

template_env = Environment(
    loader=FileSystemLoader(os.path.join(INSTALLATION_DIR, TEMPLATE_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

# ==========================================
# Setup templating filters

# def date_fmt(value):
#   return f'{value:%b %d, %Y}'

#template_env.filters['human_date'] = date_fmt


def http_fmt(value):
    locale.setlocale(locale.LC_TIME, 'en_US')
    return value.strftime('%a, %d %b %Y %H:%M:%S GMT')


template_env.filters['http_datetime'] = http_fmt

USAGE = """%prog [options] [URL...]
Scrape given URL's using user-written functions."""

def main():

    options = [
        make_option('-i', '--input',
            dest='input_file', help='Specify input file containing URL list'),
    ]

    parser = OptionParser(option_list=options, usage=USAGE)

    urls = []
    options, args = parser.parse_args()
    if len(args) > 1:
        urls = args
    elif options.input_file:
         with open(os.path.join(INSTALLATION_DIR, options.input_file)) as input_file: 
            for source in input_file:            
                source = source.strip()
                if source == '': 
                    continue # Skip empty lines
                urls.append(source)
    else:
        parser.error("no URL's or input file given")

    now = datetime.now()
    items = []
    for source in urls:            
        print(f"Fetching {source}...", end='')
        r = requests.get(source)
        print(f" got {r.status_code}")
        new_items = scrape_page(source, r.text)
        items = items + new_items
    print(f"Scraped {len(items)} items.")
    build_feed(now, items, "latest.xml")


def scrape_page(url, content):
    soup = BeautifulSoup(content, 'html.parser')
    scraper = get_scraper(url)
    items = scraper.scrape(soup)
    return items


def build_feed(now, items, output_filename):
    template = template_env.get_template('latest.xml')
    template.stream(items=items,
                    timestamp=now).dump(os.path.join(configuration.OUTPUT_DIR, output_filename))


def get_scraper(source):
    pieces = urlparse(source)
    module_name = pieces.hostname.replace(".", "_")
    try:
        scraper = importlib.import_module(f"scrapers.{module_name}")
    except (ImportError):
        raise ValueError(f"Cannot find scraper for URL {source}")
    return scraper


if __name__ == "__main__":
    main()
