#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:31:48 2017

@author: jean-marcsevin
"""

import pandas as pd

df = pd.read_csv('N201707.csv', sep=';', encoding='latin_1')
df = df.loc[:,['dep_mon', 'l_exe_spe']]

df_med = pd.read_csv('rpps-medecins-tab7.csv', sep=',', header=4, encoding='latin_1', skiprows=[5])