#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 21:48:53 2017

@author: jean-marcsevin
"""

import requests
from bs4 import BeautifulSoup

url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
years = [2010, 2011, 2012, 2013, 2014, 2015]
rows = [10, 14, 22, 27]
cells = [0, 1]

def get_soup(year):
    r = requests.get(url+str(year))
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def remove_empty_spaces(string):
    return string.replace(u'\xa0', ' ').replace(' ', '')

def select_cell(soup, tr, td):
    cells = soup.select("tr:nth-of-type("+str(tr)+") td")
    return remove_empty_spaces(cells[td].string)

for year in years:
    soup = get_soup(year)
    data_of_year = [year]
    [data_of_year.append(select_cell(soup, row, cell)) for cell in cells for row in rows]
    print(data_of_year)
