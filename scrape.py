#!/usr/bin/env python3
import os
from datetime import datetime
from urllib.parse import urlparse
from optparse import OptionParser, make_option
import importlib
import locale
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Grab this file installation directory
INSTALLATION_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = "./templates"

template_env = Environment(
    loader=FileSystemLoader(os.path.join(INSTALLATION_DIR, TEMPLATE_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

# ==========================================
# Setup templating filters
# ==========================================


def http_fmt(value):
    locale.setlocale(locale.LC_TIME, 'en_US')
    return value.strftime('%a, %d %b %Y %H:%M:%S GMT')


template_env.filters['http_datetime'] = http_fmt

USAGE = """%prog [options] [URL...]
Scrape given URL's using user-written functions and output a RSS feed."""


OPTIONS = [
    make_option('-i', '--input',
                dest='input_file', help='Specify input file containing URL list'),
    make_option('-o', '--output',
                dest='output_file', help='Specify an output file to write the RSS feed'),
]

def main():
    parser = OptionParser(option_list=OPTIONS, usage=USAGE)

    urls = []
    options, args = parser.parse_args()
    if len(args):
        urls = args
    elif options.input_file:
        with open(os.path.join(INSTALLATION_DIR, options.input_file)) as input_file:
            for source in input_file:
                source = source.strip()
                if source == '':
                    continue  # Skip empty lines
                urls.append(source)
    else:
        parser.error(
            "no URL's or input file given, use -h to show available options")

    now = datetime.now()
    items = []
    total_items = 0
    for source in urls:
        print(f"Fetching {source}...", end='')
        r = requests.get(source)
        print(f" got {r.status_code}")

        pieces = urlparse(source)
        module_name = pieces.hostname.replace(".", "_")
        try:
            scraper = importlib.import_module(f"scrapers.{module_name}")
        except ImportError:
            print(f"Cannot find scraper for URL {source}, skipped")
            continue

        new_items = scrape_page(scraper, r.text)
        items = items + [(pieces.hostname, new_items)]
        total_items = total_items + len(new_items)

    if options.output_file:
        output = open(options.output_file, "w", encoding="utf-8")
    else:
        output = open(os.path.join(os.getcwd(), 'feed.xml'),
                      "w", encoding="utf-8")

    build_feed(now, items, output)
    print(f"Written {total_items} items into {output.name}")


def scrape_page(scraper, content):
    soup = BeautifulSoup(content, 'html.parser')
    return scraper.scrape(soup)


def build_feed(now, items, output):
    template = template_env.get_template('feed.xml')
    template.stream(items=items,
                    timestamp=now).dump(output)


if __name__ == "__main__":
    main()
