#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:30:18 2017

@author: jean-marcsevin
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
from decimal import Decimal

url = 'http://www.cdiscount.com/search/10/ordinateur+'
pages_to_crawl = 5

def get_soup(brand, page):
    r = requests.get(url+brand+'.html?page='+str(page))
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def format_actual_price(item):
    return str(item).replace("<span class=\"price\">","").replace("<sup>","").replace("</sup></span>","").replace("€", ".")

def format_previous_price(item):
    return str(item).replace("<div class=\"prdtPInfoTC\">","").replace("<div class=\"prdtPrSt\">","").replace("</div>","").replace(",",".")

def get_discount_ratio_mean(brand, pages):
    discount_ratio_list = []
    
    for page in range(pages):
        soup = get_soup(brand, page)
        
        actual_price_list = [format_actual_price(item) for item in soup.select('.price')]
        previous_price_list = [format_previous_price(item) for item in soup.select('.prdtPInfoTC')]
        
        nb_products = len(actual_price_list)
        
        for i in range(nb_products):
            if previous_price_list[i] == '':
                discount_ratio_list.append(0)
            else:
                discount_ratio_list.append(1 - float(actual_price_list[i])/float(previous_price_list[i]))
                
    return str(round(Decimal(np.array(discount_ratio_list).mean()*100), 2))

print("Sur les " + str(pages_to_crawl) + " premières pages des résultats de recherche sur Cdiscount, la remise moyenne sur les ordinateurs Acer est de " + get_discount_ratio_mean('acer', pages_to_crawl) + "% tandis que celles sur les ordinateurs Dell est de " + get_discount_ratio_mean('dell', pages_to_crawl)+"%.")
