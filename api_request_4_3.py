# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:14:00 2023

@author: tup13970
"""

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
import warnings
import indices_constants

# In[2]:

def get_api_data(state, county, years, indices):
    
    ##years##
    
    #sort years
    years.sort()
    
    no_data_yrs = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008]
    
    for year in years:
        if (int(year) in no_data_yrs) or int(year) < 2000: 
            raise ValueError("This function cannot retrieve data for years before 2000 or from 2001-2005")
    
    ##Bates errors##
    if ("bates" in indices) and (len(years) < 3):
        raise Exception("to calculate the Bates-Freeman indices, you must input three years")
        
    if ("bates" in indices) and ((int(years[1]) - int(years[0]) < 10) or (int(years[2])- int(years[1]))):
        warnings.warn("The methodology used in Bates(2013) used three study years, each 10 years apart. If you use the resulting df from this function to calculate the Bates-Freeman indices, be aware that are using a different interval between study years.")
        
    
    
    
    def bates_home_value_index(year, state, county):
        if year == 2000:
            HOST = "https://api.census.gov/data"
            year = "{year}"
            dataset = "dec/sf3?"
            census_base_url_2000 = "/".join([HOST, year, dataset])
            predicates = {}
            predicates["get"] = 'H085001'
            predicates["for"] = "tract:*"
            predicates["in"] = f"state:{state}, county:{county}"
            #predicates["key"] = ____________________
            a = requests.get(census_base_url_2000, params=predicates).json()
            census_df = pd.DataFrame(data=a[1:], columns = a[0]).rename(columns = master_decennial_dict, inplace=True)
            return census_df
        else:
            HOST = "https://api.census.gov/data"
            year = "{year}"
            dataset = "acs/acs5"
            bates_hvi_url = "/".join([HOST, year, dataset])
            predicates = {}
            predicates["get"] = 'B25077_001E'
            predicates["for"] = "tract:*"
            predicates["in"] = f"state:{state}, county:{county}"
            #predicates["key"] = ____________________
            x = requests.get(bates_hvi_url, params=predicates).json()
            hvi_df = pd.DataFrame(data=x[1:], columns = x[0]).rename(columns = master_tract_dict, inplace=True)
            return hvi_df
    
    def bates_vars_yr1(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        bates_vars_yr1 = ['B25003_001E', 'B25003_002E',  
                      'B25003_003E', 'B03002_001E',  
                      'B03002_003E','S1501_C01_006E',
                      'S1501_C01_012E', 'B19113_001E', 
                      'B19013_001E', 'B25077_001E']
        predicates = {}
        predicates["get"] = ",".join(bates_vars_yr1)
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        b = requests.get(acs_base_url, params=predicates).json()
        bates_vars_yr1_df = pd.DataFrame(data=b[1:], columns=b[0]).rename(columns = master_tract_dict, inplace=True)
        return bates_vars_yr1_df
    
    def bates_vars_yr2(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        bates_vars_yr2 = ['B25003_001E', 'B25003_002E',  
                      'B25003_003E', 'B03002_001E',  
                      'B03002_003E','S1501_C01_006E',
                      'S1501_C01_012E', 'B19113_001E', 
                      'B19013_001E', 'B25077_001E']
        predicates = {}
        predicates["get"] = ",".join(bates_vars_yr2)
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        c = requests.get(acs_base_url, params=predicates).json()
        bates_vars_yr2_df = pd.DataFrame(data=c[1:], columns=c[0]).rename(columns = master_tract_dict, inplace=True)
        return bates_vars_yr2_df
    
    def bates_vars_area_yr1(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        bates_vars_area_yr1 = ['B19013_001E','B19013_001M', 'B19113_001E', 'B19113_001M']
        predicates = {}
        predicates["get"] = ",".join(bates_vars_area_yr1)
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        d = requests.get(acs_base_url, params=predicates).json()
        bates_vars_area_yr1_df = pd.DataFrame(data=d[1:], columns=d[0]).rename(columns = master_county_dict, inplace=True)
        return bates_vars_area_yr1_df
    
    def bates_vars_area_yr2(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        bates_vars_area_yr2 = ['B19013_001E','B19013_001M', 'B19113_001E', 'B19113_001M']
        predicates = {}
        predicates["get"] = ",".join(bates_vars_area_yr2)
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        e = requests.get(acs_base_url, params=predicates).json()
        bates_vars_area_yr2_df = pd.DataFrame(data=e[1:], columns=e[0]).rename(columns = master_county_dict, inplace=True)
        return bates_vars_area_yr2_df
    
    def ding_vars_request_yr1(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        predicates = {}
        predicates["get"] = ",".join('B25064_001E', 'B25077_001E',
               'S1501_C01_001E', 'S1501_C01_006E',
               'S1501_C01_005E', 'S1501_C01_012E',
               'B19013_001E')
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        f = requests.get(acs_base_url, params=predicates).json()
        ding_vars_request_yr1_df = pd.DataFrame(data=f[1:], columns=f[0]).rename(columns = master_tract_dict, inplace=True)
        return ding_vars_request_yr1_df
    
    def ding_vars_request_yr2(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        predicates = {}
        predicates["get"] = ",".join('B25064_001E', 'B25077_001E',
               'S1501_C01_001E', 'S1501_C01_006E',
               'S1501_C01_005E', 'S1501_C01_012E',
               'B19013_001E')
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        g = requests.get(acs_base_url, params=predicates).json()
        ding_vars_request_yr2_df = pd.DataFrame(data=g[1:], columns=g[0]).rename(columns = master_tract_dict, inplace=True)
        return ding_vars_request_yr2_df
    
    def ding_vars_area_request_yr1(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        predicates = {}
        predicates["get"] = ",".join('B25064_001E', 'B25077_001E', 'B19013_001E')
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        h = requests.get(acs_base_url, params=predicates).json()
        ding_vars_area_request_yr1_df = pd.DataFrame(data=h[1:], columns=h[0]).rename(columns = master_county_dict, inplace=True)
        return ding_vars_area_request_yr1_df
    
    def ding_vars_area_request_yr2(year, state, county):
        HOST = "https://api.census.gov/data"
        year = "{year}"
        dataset = "acs/acs5"
        acs_base_url = "/".join([HOST, year, dataset])
        predicates = {}
        predicates["get"] = ",".join('B25064_001E', 'B25077_001E', 'B19013_001E')
        predicates["for"] = "tract:*"
        predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
        i = requests.get(acs_base_url, params=predicates).json()
        ding_vars_area_request_yr2_df = pd.DataFrame(data=i[1:], columns=i[0]).rename(columns = master_county_dict, inplace=True)
        return ding_vars_area_request_yr2_df
    
    
    #def acs_request(year, state, county):
       # HOST = "https://api.census.gov/data"
       # year = "{year}"
       # dataset = "acs/acs5"
       # acs_base_url = "/".join([HOST, year, dataset])
       # predicates = {}
       # predicates["get"] = ",".join()
       # predicates["for"] = "tract:*"
       # predicates["in"] = f"state:{state}, county:{county}"
        #predicates["key"] = ____________________
       # j = requests.get(acs_base_url, params=predicates).json()
       # acs_df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict, inplace=True)
       # return acs_df
    
    def tiger_request(year, state, county):
        url = f'https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state}_tract.zip'
        extract_to='.'
        t_response = urllib.request.urlopen(url)
        zipfile = ZipFile(BytesIO(t_response.read()))
        zipfile.extractall(path=extract_to)
        t_df = gpd.read_file(f'tl_{year}_{state}_tract.shp')
        t_df = t_df.set_geometry('geometry')
        t_df = t_df.rename(columns = {'TRACTCE':'tract'})
        t_df = t_df[t_df['COUNTYFP'] == {county}]
        return t_df
    
    
    if index == f'{index_name}':
        ding_df = pd.merge(ding_vars_request_yr1_df, ding_vars_request_yr2_df, 
                           ding_vars_area_request_yr1_df, ding_vars_area_request_yr2_df, t_df)
        return ding_df
    elif index == 'bates-freeman':
        bates_freeman_df = pd.merge(bates_vars_area_yr1_df, bates_vars_area_yr2_df, 
                                    bates_vars_yr2_df, bates_vars_yr2_df, t_df)
        return bates_freeman_df
    
    




