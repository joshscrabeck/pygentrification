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
import warnings
from tobler.area_weighted import area_interpolate
from functools import reduce
from indices_constants import ding_vars, ding_vars_area, bates_vars_acs_yr0, bates_vars_census_yr0, bates_vars_yr1, bates_vars_yr2, bates_vars_area, master_county_dict, master_tract_dict
from harmonize_tracts_func import harmonize_tracts

# HOST = "https://api.census.gov/data"
# year = "2020"
# dataset = "acs/acs5"
# acs_base_url = "/".join([HOST, year, dataset])

# print(acs_base_url)

# HOST = "https://www2.census.gov/geo/tiger/TIGER2020/TRACT"
# dataset = "tl_2020_42_tract.zip"
# tiger_2020_url = "/".join([HOST, dataset])

# HOST = "https://api.census.gov/data"
# year = "2010"
# dataset = "acs/acs5"
# acs_base_url_2010 = "/".join([HOST, year, dataset])
# print(acs_base_url_2010)

# HOST = "https://api.census.gov/data"
# year = "2000"
# dataset = "dicennial/dicennial"
# census_base_url_2000 = "/".join([HOST, year, dataset])

# print(census_base_url_2000)


# In[6]:


# bates_vars = {'codes':['B25003_001E', 'B25003_001M', 
#                        'B25003_002E', 'B25003_002M', 
#                        'B25003_003E', 'B25003_003M', 
#                        'B03002_001E', 'B03002_001M', 
#                        'B03002_003E', 'B03002_003M', 
#                        'B15002_001E', 'B15002_001M', 'B15002_002E', 
#                        'B15002_002M', 'B15002_014E', 'B15002_014M', 
#                        'B15002_015E', 'B15002_015M', 'B15002_016E', 
#                        'B15002_016M', 'B15002_017E', 'B15002_017M', 
#                        'B15002_018E', 'B15002_018M','B15002_019E', 
#                        'B15002_019M', 'B15002_031E', 'B15002_031M', 
#                        'B15002_032E', 'B15002_032M', 'B15002_033E', 
#                        'B15002_033M', 'B15002_034E', 'B15002_034M', 
#                        'B15002_035E', 'B15002_035M',
#                        'B19113_001E', 'B19113_001M',
#                        'B19013_001E', 'B19013_001M',
#                        'B25077_001E', 'B25077_001M',
#                        'B25034_001E', 'B25034_001M',
#                        'B25034_002E', 'B25034_002M',
#                        'B25034_003E', 'B25034_003M'],
#               'columns': ['pop_ten','pop_ten_e', 'owner', 'owner_e', 'renter', 'renter_e',
#                           'poprac', 'poprac_e', 'white', 'white_e', 'popedu', 'popedu_e',
#                           'popedum', 'popedum_e', 'ASdegm', 'ASdegm_e', 'BAdegm', 'BAdegm_e',
#                           'MAdegm', 'MAdegm_e', 'prodegm', 'prodegm_e', 'drdegm',
#                           'drdegme', 'popeduf', 'popeduf_e', 'ASdegf', 'ASdegf_e',
#                           'BAdegf', 'BAdegf_e', 'MAdegf', 'MAdegf_e', 'prodegf',
#                           'prodegf_e', 'drdegf', 'drdegf_e', 'mfi', 'mfi_e', 'mhi', 'mhi_e',
#                           'mhv', 'mhv_e', 'tothous', 'tothous_e', 'y14topr', 'y14topr_e',
#                           'y10to13', 'y10to13_e',]}

# test_vars = {'B25064_001E': 'med_rent_1', 'B25077_001E': 'med_home_val_1',
#        'S1501_C01_001E': '18_24_pop_1'}

def acs_request_tract(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    #print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
    #predicates["key"] = ____________________
    j = requests.get(acs_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict, inplace=True)
    return df

def acs_request_area(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = "{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    #print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = f"county:{county}"
    predicates["in"] = f"state:{state}"
    #predicates["key"] = ____________________
    j = requests.get(acs_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict, inplace=True)
    return df

# HOST = "https://api.census.gov/data"
# year = "2000"
# dataset = "dicennial/dicennial"
# census_base_url_2000 = "/".join([HOST, year, dataset])

def census_request_tract(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dicennial/dicennial"
    census_base_url_2000 = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = f"county:{county}"
    predicates["in"] = f"state:{state}"
    j = requests.get(census_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict, inplace=True)
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

def get_api_data_tract(state, county, years, indices):
    
    ###Check input###
    
    #Years
    
    #sort years
    years.sort()
    
    no_data_yrs = [2001, 2002, 2003, 2004, 2005]
    
    for year in years:
        if (int(year) in no_data_yrs) or int(year) < 2000: 
            raise ValueError("This function cannot retrieve data for years before 2000 or from 2001-2005")
    
    #Bates errors
    if ("bates" in indices) and (len(years) < 3):
        raise Exception("to calculate the Bates-Freeman indices, you must input three years")
        
    if ("bates" in indices) and ((int(years[1]) - int(years[0]) < 10) or (int(years[2])- int(years[1]))):
        warnings.warn("The methodology used in Bates(2013) used three study years, each 10 years apart. If you use the resulting df from this function to calculate the Bates-Freeman indices, be aware that are using a different interval between study years.")
        
    
    ###Set up varcodes###
    
    
    #Initialize empty list for yr 1 and 2 varcodes
    var_codes_yr1=[]
    var_codes_yr2=[]
    
    
    #loop through indices list
        for index in indices:
        
        #if ding
        
            #for loop through ding_vars
                #append item in list to var_codes_yr_1
                #append item in list to var_codes_yr_2
    
    
        #if bates
        if index == "bates":
            for varcode in bates_vars_yr1:
                var_codes.append(varcode)
            for varcode in bates_vars_yr2:
                var_codes.append(varcode)
            
            if int(years[0]) == 2000:
                var_codes_yr0 = bates_vars_census_yr0    
                    
            else:
                var_codes_yr0 = bates_vars_acs_yr0
                    
        
        #drop duplicates
        var_codes_yr1 = list(set(var_codes_yr1))
        var_codes_yr2 = list(set(var_codes_yr2))
                
        
    ###api calls###
    
    #initialize empty list df_list
    
    ##Year 0##
    
    #if len(years) > 2:
    
        #if year[0] is 2000
    
            #assign census_df_yr0 to output of census_request_tract function for 2000 and var_codes_yr0
        
            #assign tiger_df_yr0 to output of tiger_request for 2000
        
            #merge and assign to df_yr0
        
            #append df_year0 to df_list
            
        #else
        
            #assign acs_df_yr0 to output of acs_request_tract function for years[0] and var_codes_yr0
            
            #assign tiger_df_yr0 to output of tiger_request for years[0]
        
            #merge and assign to df_yr0
        
            #append df_year0 to df_list
            
    ##Year 1##
        
        #assign acs_df_yr1 to output of acs_request_tract function for years[1] and var_codes_yr1
        
        #assign tiger_df_yr1 to output of tiger_request for years[1]
    
        #merge and assign to df_yr1
    
        #append df_yr1 to df_list
        
    ##Year 2##
        
        #assign acs_df_yr2 to output of acs_request_tract function for years[2] and var_codes_yr2
        
        #assign tiger_df_yr2 to output of tiger_request for years[2]
    
        #merge and assign to df_yr2
    
        #append df_yr2 to df_list
        
    
    ###Harmonize dataframes to the tracts in year 2###

    target_df = df_list[-1]
    input_dfs = df_list[0:-1]
    
    df = harmonize_tracts(target_df, input_dfs)
       
              
    return df

    

