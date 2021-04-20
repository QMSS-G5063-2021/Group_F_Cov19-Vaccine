#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 21:21:30 2021

@author: belindawu
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime as dt
import fnmatch
import glob
import re
import requests

def access_data():
    r = requests.get('https://api.nytimes.com/svc/archive/v1/2020/9.json?api-key=f1jfaycbADmZ3Qf9i1Wo9YBeSZtonAG4')
    if r.status_code != 200:
        print("fail to access to API")
        sys.exit()
    elif r.status_code == 200:
        print("successful!")
    data_json = r.json()
    return(data_json)

datainjson = access_data()
datainjson

def transform_format(value):
    data_dataframe = pd.DataFrame(value)
    return data_dataframe

data_dataframe = transform_format(datainjson)
data_dataframe

def show_the_keys():
    data_keys = data_dataframe['response'].keys()
    return data_keys

show_the_keys()

def focus_on_results(value):  
    the_results = pd.DataFrame(data_dataframe['response'][0])
    return the_results

results = focus_on_results('results')
results

results['lead_paragraph'][0]


results.to_csv('nyt202009.csv')