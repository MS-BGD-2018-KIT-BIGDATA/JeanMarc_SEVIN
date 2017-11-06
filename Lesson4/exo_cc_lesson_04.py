#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:16:15 2017

@author: jean-marcsevin
"""

import requests
import pandas as pd
import re

test = requests.get('https://www.open-medicaments.fr/api/v1/medicaments/63605055').json()
labo = test['titulaires']
libelle = test['presentations'][0]['libelle']

def get_meds():
    r = requests.get('https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprofene&limit=100')
    return r.json()

df = pd.DataFrame([[med['codeCIS'], med['denomination']] for med in get_meds()])

# df = pd.read_csv('CIS_bdpm.txt', sep='\t')

regex = re.compile('\d+')
dosage_par_unite = int(regex.findall(test['denomination'])[0])
nombre_unite_par_boite = int(regex.findall(libelle)[0])