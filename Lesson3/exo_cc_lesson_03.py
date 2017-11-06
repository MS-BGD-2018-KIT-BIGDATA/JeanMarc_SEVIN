#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:36:13 2017

@author: jean-marcsevin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.insee.fr/fr/statistiques/1906659'

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def clean_commune(item):
    return str(item).replace("<th class=\"ligne \" scope=\"row\">","").replace("</th>","")

def calc_distance(origin, destination):
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origin + "&destinations=" + destination + "&language=fr-FR&key=AIzaSyDhnRwPrt4EQqiQg3Q-hNcAXsk0Iy5qCcg")
    return r.json()['rows'][0]['elements'][0]['distance']['text']

soup = get_soup(url)

communes_raw = soup.find('table', attrs={"id": "produit-tableau-T16F014T4"}).find('tbody').find_all('th')[1::2]
communes = [clean_commune(item) for item in communes_raw]

nb_Communes = len(communes)

df = pd.DataFrame(index=communes, columns=communes)

# Il manque la routine pour construire la matrice et l'exporter au format CSV        