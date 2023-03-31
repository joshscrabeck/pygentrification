#!/usr/bin/env python
# coding: utf-8

#%%

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
from indices_constants import ding_vars, ding_vars_area, bates_vars_acs_yr0, bates_vars_census_yr0, bates_vars_yr1, bates_vars_yr2, bates_vars_area_yr1, bates_vars_area_yr2, master_county_dict, master_tract_dict
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


#%%

###api request base functions###

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
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_county_dict, inplace=True)
    return df


def census_request_tract(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dicennial/dicennial"
    census_base_url = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
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

#%%

###comprehensive api call function for tract-level###

def get_api_data_tract(state, county, years, indices):
     
    ###check input###
    
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
        
    
    ###set up varcodes###
    
    
    #Initialize lists for yr 1 and 2 varcodes
    var_codes_yr1=[]
    var_codes_yr2=['B03002_001E','B25034_001E'] #initialize with vars for total population and total housing units, which will be used to filter census tracts
    
    
    #loop through indices list
    for index in indices:
        
        #if ding
        
            #for loop through ding_vars
                #append item in list to var_codes_yr_1
                #append item in list to var_codes_yr_2
    
    
        #if bates
        if index == "bates":
            for varcode in bates_vars_yr1:
                var_codes_yr1.append(varcode)
                
            for varcode in bates_vars_yr2:
                var_codes_yr2.append(varcode)
            
            if int(years[0]) == 2000:
                var_codes_yr0 = bates_vars_census_yr0    
                    
            else:
                var_codes_yr0 = bates_vars_acs_yr0
                    
        
        #drop duplicates
        var_codes_yr1 = list(set(var_codes_yr1))
        var_codes_yr2 = list(set(var_codes_yr2))
                
        
    ###api calls###
    
    #initialize empty list df_list
    
    ##year 0##
    
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
            
    ##year 1##
        
        #assign acs_df_yr1 to output of acs_request_tract function for years[1] and var_codes_yr1
        
        #assign tiger_df_yr1 to output of tiger_request for years[1]
    
        #merge and assign to df_yr1
    
        #append df_yr1 to df_list
        
    ##year 2##
        
        #assign acs_df_yr2 to output of acs_request_tract function for years[2] and var_codes_yr2
        
        #assign tiger_df_yr2 to output of tiger_request for years[2]
    
        #merge and assign to df_yr2
    
        #append df_yr2 to df_list
        
    
    ###Harmonize dataframes to the tracts in year 2 and filter###

    target_df = df_list[-1]
    input_dfs = df_list[0:-1]
    
    df = harmonize_tracts(target_df, input_dfs)
    
    #filter out tracts that have 0 housing units and/or less than 50 people. 
    #pop_race_yr2 is the total populationf for year 2. tot_house_yr2 is the total number of houseing units in year 2.

    df = df.loc[(df['pop_race_yr2'] >= 50) & (df['tot_house_yr2'] > 0)]
           
              
    return df

#%%
    
###comprehensive api call function for county-level###

def get_api_data_county(state, county, years, indices):
    
    #sort years
    years.sort()
    
    ###check input###
    
    for year in years:
        if int(year) < 2009:
            raise ValueError("This function retrieves American Community Survey 5-yr estimates data and cannot retrieve data for years before 2009")
        if len(years) != 2:
            raise ValueError("This years parameter requires a list of length 2. ")
    
    ###set up varcodes###
    #Initialize lists for yr 1 and 2 varcodes
    
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
            for varcode in bates_vars_area_yr1: 
                var_codes_yr1.append(varcode) 
            for varcode in bates_vars_area_yr2: 
                var_codes_yr2.append(varcode)
                
    #drop duplicates
    var_codes_yr1 = list(set(var_codes_yr1)) 
    var_codes_yr2 = list(set(var_codes_yr2))
    
    
    ###api calls###
    
    
    ##year 1##
    
        #assign df_yr1 to output of acs_request_area function for years[1] and var_codes_yr1
        
        #drop all columns except acs variables and add suffix _yr1
        #.add_suffix('_yr1')
        
    ##year 2##
    
        #assign df_yr2 to output of acs_request_area function for years[2] and var_codes_yr2
        
        #drop all columns except acs variables and GEOID and add suffix _yr2
        #.add_suffix('_yr2')
        
        #merge two dfs by index  and assign to df
        
    return df    
            
            
            
            
            
            
            
            

