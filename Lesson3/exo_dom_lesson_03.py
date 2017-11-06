#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:49:57 2017

@author: jean-marcsevin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://gist.github.com/paulmillr/2657075'

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_repos(user):
    r = requests.get('https://api.github.com/users/' + user + '/repos', {'type': 'owner'}, auth = ('jmsevin', '7a48e19ed3b70887e57a25694e3e42b916a70244'))
    return r.json()

def calc_stars_mean(repos):
    sm = pd.Series([repo['stargazers_count'] for repo in repos]).mean()
    return sm

def get_user_stars_mean(user):
    usm = calc_stars_mean(get_repos(user))
    return usm
    
soup = get_soup(url)

rows = soup.find('tbody').find_all('tr')
users = [row.find('a').text for row in rows]
stars = [calc_stars_mean(get_repos(user)) for user in users]

classement = pd.DataFrame({'Utilisateur': users, 'Moyenne': stars})
classement = classement[['Utilisateur', 'Moyenne']].sort_values('Moyenne', ascending = False)