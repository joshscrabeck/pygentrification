#!/usr/bin/env python
# coding: utf-8

# In[3]:

#HUD CHAS API Token
##eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMyZmNmNzI5NDg5NzZkMmUyNjM4MWM1ZGUxNDMyYjIwZTBjM2ViNGYxMGJiN2IzZWU2NWFiOWQ0YTIzNWFhYjI5MTRjM2MzNTNiNTYzY2ZjIn0.eyJhdWQiOiI2IiwianRpIjoiMzJmY2Y3Mjk0ODk3NmQyZTI2MzgxYzVkZTE0MzJiMjBlMGMzZWI0ZjEwYmI3YjNlZTY1YWI5ZDRhMjM1YWFiMjkxNGMzYzM1M2I1NjNjZmMiLCJpYXQiOjE2NzY5NDUyMDIsIm5iZiI6MTY3Njk0NTIwMiwiZXhwIjoxOTkyNTY0NDAyLCJzdWIiOiI0NzI2MSIsInNjb3BlcyI6W119.KXmlEzT08PT4mnJjYLNPhdGSFgDS-LYlpZn5ZpTjuN0lZFBM9ixZA0V1wlpcx99aIVSR3K6Cc2ixsT4ryXUsAA

import os
from io import BytesIO
import requests
import numpy
import pandas as pd
import json
from zipfile import ZipFile
from pprint import pprint
import urllib
import shutil
import geopandas as gpd

HOST = "https://api.census.gov/data"
year = "2020"
dataset = "acs/acs5"
acs_base_url = "/".join([HOST, year, dataset])

print(acs_base_url)

HOST = "https://www2.census.gov/geo/tiger/TIGER2020/TRACT"
dataset = "tl_2020_42_tract.zip"
tiger_2020_url = "/".join([HOST, dataset])

HOST = "https://api.census.gov/data"
year = "2010"
dataset = "acs/acs5"
acs_base_url_2010 = "/".join([HOST, year, dataset])
print(acs_base_url_2010)

HOST = "https://api.census.gov/data"
year = "2000"
dataset = "dicennial/dicennial"
census_base_url_2000 = "/".join([HOST, year, dataset])

print(census_base_url_2000)


# In[6]:


bates_vars = {'codes':['B25003_001E', 'B25003_001M', 
                       'B25003_002E', 'B25003_002M', 
                       'B25003_003E', 'B25003_003M', 
                       'B03002_001E', 'B03002_001M', 
                       'B03002_003E', 'B03002_003M', 
                       'B15002_001E', 'B15002_001M', 'B15002_002E', 
                       'B15002_002M', 'B15002_014E', 'B15002_014M', 
                       'B15002_015E', 'B15002_015M', 'B15002_016E', 
                       'B15002_016M', 'B15002_017E', 'B15002_017M', 
                       'B15002_018E', 'B15002_018M','B15002_019E', 
                       'B15002_019M', 'B15002_031E', 'B15002_031M', 
                       'B15002_032E', 'B15002_032M', 'B15002_033E', 
                       'B15002_033M', 'B15002_034E', 'B15002_034M', 
                       'B15002_035E', 'B15002_035M',
                       'B19113_001E', 'B19113_001M',
                       'B19013_001E', 'B19013_001M',
                       'B25077_001E', 'B25077_001M',
                       'B25034_001E', 'B25034_001M',
                       'B25034_002E', 'B25034_002M',
                       'B25034_003E', 'B25034_003M'],
              'columns': ['pop_ten','pop_ten_e', 'owner', 'owner_e', 'renter', 'renter_e',
                          'poprac', 'poprac_e', 'white', 'white_e', 'popedu', 'popedu_e',
                          'popedum', 'popedum_e', 'ASdegm', 'ASdegm_e', 'BAdegm', 'BAdegm_e',
                          'MAdegm', 'MAdegm_e', 'prodegm', 'prodegm_e', 'drdegm',
                          'drdegme', 'popeduf', 'popeduf_e', 'ASdegf', 'ASdegf_e',
                          'BAdegf', 'BAdegf_e', 'MAdegf', 'MAdegf_e', 'prodegf',
                          'prodegf_e', 'drdegf', 'drdegf_e', 'mfi', 'mfi_e', 'mhi', 'mhi_e',
                          'mhv', 'mhv_e', 'tothous', 'tothous_e', 'y14topr', 'y14topr_e',
                          'y10to13', 'y10to13_e',]}

test_vars = {'B25064_001E': 'med_rent_1', 'B25077_001E': 'med_home_val_1',
       'S1501_C01_001E': '18_24_pop_1'}

def acs_request(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = "{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
    #predicates["key"] = ____________________
    j = requests.get(acs_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_dict, inplace=True)
    return df

def tiger_request(year, state, county):
    url = f'https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state}_tract.zip'
    extract_to='.'
    t_response = urllib.request.urlopen(url)
    zipfile = ZipFile(BytesIO(t_response.read()))
    zipfile.extractall(path=extract_to)
    t_df = gpd.read_file(f'tl_{year}_{state}_tract.shp')
    t_df = t_df.set_geometry('geometry')
    t_df = t_df.rename(columns = {'TRACTCE':'tract'})
    t_df = dict(filter({county}))
    return t_df

def merge(acs_df, t_df):
    complete_df=pd.merge(t_df, acs_df)
    return complete_df

def get_api_data(state, county, years, index):
    
    
    var_codes=[]
    col_names=[]
    
    #if index = master:
        #vars = master_vars
       
        
    for yr in years:
        acs_df = acs_request(year, state, county, var_codes, col_names)
        tig_df = tiger_request(year, state, county)
    
             
    return df




#### use library urllib will read a data stream (chapter 20 in GIS programming textbook)
### return a dataframe, (dataframe creation data = r.json()[1:])
    

#use geosnap for 1990-2010, tiger census for 2020 geometries.
#harmonize.harmonize(gdf[, target_year, ...]) ,
#Use spatial interpolation to standardize neighborhood boundaries over time.
