#!/usr/bin/env python
# coding: utf-8
import argparse
import datetime
import os
import requests
import sys
import textwrap
from bs4 import BeautifulSoup
from random import randint

# Parse output path argument for script
scriptinfo = 'Scrape and parse Wikipedia history information'
parser = argparse.ArgumentParser(description=scriptinfo)
out_help = 'Directory where output from script will be saved'
parser.add_argument('outputpath', help=out_help)
width_help = 'Length of lines in output'
parser.add_argument('width', nargs='?', const=54, type=int,
                    default=54, help=width_help)
args = parser.parse_args()

WIKIPEDIA = 'https://en.wikipedia.org/wiki/Main_Page'
TODAY = '{:%B_%-d}'.format(datetime.datetime.now())


def wikiscrape(today, width):
    """
    Scrapes all anniversary events for a date from Wikipedia
    and prints events at random.

    Args:
        today (str): A date formatted as '{:%B_%-d}'
            Example: 'November_2'
        width (int): Width of formatting for output, measured
            as the number of characters. Default value is 54.

    Returns:
        str: A paragraph of the selected historical event.
            Maximum length of six lines; if text is longer then
            the last line is deleted from paragraph.

    """
    wiki_today_url = 'https://en.wikipedia.org/wiki/' + today

    wiki_today = BeautifulSoup(requests.get(wiki_today_url).text, 'lxml')

    events_raw = wiki_today.find(id='Events').findNext('ul')('li')
    # NOTE: I am drawing a random event, with replacement.
    #       This will lead to some historical events appearing repeatedly.
    #       I thought about drawing Wikipedia entries without replacement,
    #       but it isn't a high priority for me.
    event = events_raw[(randint(0, len(events_raw)-1))].text
    # Deal with weird spacing issues
    for ch in [' ', ' ']:
        if ch in event:
            event.replace(ch, ' ')
    dedented_text = textwrap.dedent(event).strip()
    wrapped_text = textwrap.fill(dedented_text, width=width)
    # Cut off the last sentence if the text goes beyond 6 lines.
    if wrapped_text.count('\n') >= 6:
        wrapped_text = '. '.join(wrapped_text.split('. ')[:-1])+'.'
    # Replace '$' with '$$' to prevent Conky reading errors
    wrapped_text = wrapped_text.replace('$', '$$')
    return wrapped_text


if __name__ == "__main__":
    # Check that we have internet connection
    try:
        response = requests.get(WIKIPEDIA)
    except Exception as e:
        sys.exit()
    wrapped_text = wikiscrape(TODAY, args.width)
    # Change directory
    os.chdir(args.outputpath)

    text = open("history", "w")
    text.write(wrapped_text)
    text.close()
