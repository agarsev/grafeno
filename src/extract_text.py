#!/usr/bin/env python3

from bs4 import BeautifulSoup

def html_to_text (html):
    '''Takes an html document and extracts the body text'''
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find(id='story-body')
    if not body:
        body = soup.find(id='mw-content-text')
    if not body:
        body = soup.find(class_='story-body')
    if not body:
        body = soup.find('body')
    return u' '.join(p.get_text() for p in body.find_all('p'))

if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Extract the body text of an html document')
    arg_parser.add_argument('doc', help='document')
    args = arg_parser.parse_args()

    with open(args.doc, mode='r') as f:
        print(html_to_text(f.read()))

