#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:31:48 2017

@author: jean-marcsevin
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import random
import time

regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
annonces = pd.DataFrame(columns = ['Titre', 'Version', 'Année', 'Kilométrage', 'Prix', 'Type', 'Cote'])

def get_nb_pages(region) :
    url = 'https://www.leboncoin.fr/voitures/offres/' + region + '/?th=1&brd=Renault&mdl=Zoe'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    link2last = soup.find('a', {'id': 'last'})['href']
    nb_pages = re.sub(r'[^0-9]','',link2last)
    return int(nb_pages)

def get_ads_soup(region, page):
    url = 'https://www.leboncoin.fr/voitures/offres/' + region + '/?o=' + str(page) + '&brd=Renault&mdl=Zoe'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_car_infos(url_page):
    r = requests.get(url_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    description = str(soup.find('p', {'itemprop': 'description'})).lower()
    version = get_version_from_desc(description)
    infos = soup.find_all('span', {'class': 'value'})
    annee = re.sub(r'[^0-9]','',str(infos[4]))
    kilometrage = re.sub(r'[^0-9]','',str(infos[5]))
    prix = re.sub(r'[^0-9]','',str(infos[0]))
    return {'Version':version, 'Année':annee, 'Kilométrage':kilometrage, 'Prix': prix}

def get_version_from_desc(description):
    if 'zen' in description:
        return 'Zen'
    elif 'life' in description:
        return 'Life'
    elif 'intens' in description:
        return 'Intens'
    else:
        return 'Modèle non renseigné'
    
def get_cote(version, annee):
    url = 'https://www.lacentrale.fr/cote-auto-renault-zoe-' + version + '-' + annee + '.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    cote = str(soup.find('span', {'class': 'jsRefinedQuot'})).replace('<span class="jsRefinedQuot">', '').replace('</span>', '').replace(' ', '')
    return cote

for region in regions :
    for page in range(get_nb_pages(region)):
        ads_soup = get_ads_soup(region, page)
        ads = ads_soup.find_all('a', {'class': 'list_item clearfix trackable'})
        for ad in ads:
            time.sleep(random.randint(1, 10))
            car_infos = get_car_infos('http:' + ad['href'])
            cote = get_cote(car_infos['Version'], car_infos['Année'])
            annonces.loc[len(annonces)] = [ad['title'], car_infos['Version'], car_infos['Année'], car_infos['Kilométrage'], car_infos['Prix'], eval(ad['data-info'])['ad_offres'], cote]

annonces['Type'] = annonces['Type'].replace('pro', 'Professionnel').replace('part', 'Particulier')
annonces['Supérieur à l\'argus']=(annonces['Prix']>annonces['Cote'])

annonces.to_csv('annonces.csv')