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
