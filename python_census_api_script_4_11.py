#!/usr/bin/env python
# coding: utf-8

#%%
from io import BytesIO
import requests
import pandas as pd
import json
from zipfile import ZipFile
import urllib
import geopandas as gpd
import warnings
from indices_constants import ding_vars, ding_vars_area, bates_vars_acs_yr0, bates_vars_census_yr0, bates_vars_yr1, bates_vars_yr2, bates_vars_area_yr1, bates_vars_area_yr2, master_county_dict, master_tract_dict
from harmonize_tracts_func_final import harmonize_tracts


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
    r = requests.get(acs_base_url, params=predicates)
    j = r.json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict)
    df['GEOID'] = df['state']+df['county']+df['tract']
    df = df.drop(columns = ['state', 'county', 'tract'])
    return df

def acs_request_area(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    #print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = f"county:{county}"
    predicates["in"] = f"state:{state}"
    #predicates["key"] = ____________________
    j = requests.get(acs_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_county_dict)
    return df


def census_request_tract(year, state, county, index_vars):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dec/sf3?"
    census_base_url = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(index_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
    j = requests.get(census_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict)
    df['GEOID'] = df['state']+df['county']+df['tract']
    df = df.drop(columns = ['state', 'county', 'tract'])
    return df

def tiger_request(year, state, county):
    if int(year) < 2010:
        url = f'https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2000/tl_2010_{state}{county}_tract00.zip'
    elif int(year) < 2020:
        url = f'https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_{state}{county}_tract10.zip'
    else:
        url = f'https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state}_tract.zip'
    extract_to='.'
    t_response = urllib.request.urlopen(url)
    zipfile = ZipFile(BytesIO(t_response.read()))
    zipfile.extractall(path=extract_to)
    if int(year) < 2010:
        t_df = gpd.read_file(f'tl_2010_{state}{county}_tract00.shp')
        t_df = t_df.rename(columns = {'TRACTCE':'tract', 'CTIDFP00':'GEOID'})
    elif int(year) < 2020:
        t_df = gpd.read_file(f'tl_2010_{state}{county}_tract10.shp')
        t_df = t_df.rename(columns = {'TRACTCE':'tract', 'GEOID10':'GEOID'})
    else:        
        t_df = gpd.read_file(f'tl_{year}_{state}_tract.shp')
        t_df = t_df.rename(columns = {'TRACTCE':'tract'})
        t_df = t_df[t_df['COUNTYFP'] == f'{county}'] 
    t_df = t_df.set_geometry('geometry')
    t_df = t_df[['GEOID', 'geometry']]
    t_df = t_df.reset_index(drop = True)
    return t_df

def tract_merge(acs_df, t_df):
    acs_df = acs_df.drop(columns = ['GEOID'])
    df=pd.merge(t_df, acs_df, left_index = True, right_index =  True)
    df = df[(df != '-666666666').all(axis = 1)]
    #df = df[(df['med_rent'] != '-666666666') & (df['med_fam_inc'] != '-666666666') & (df['med_home_val'] != '-666666666') & (df['med_house_inc'] != '-666666666')]
    return df

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
        
    if ("bates" in indices) and ((int(years[1]) - int(years[0]) < 10) or (int(years[2])- int(years[1])) < 10):
        warnings.warn("The methodology used in Bates(2013) used three study years, each 10 years apart. If you use the resulting df from this function to calculate the Bates-Freeman indices, be aware that are using a different interval between study years.")
        
    
    ###set up varcodes###
    
    
    #Initialize lists for yr 1 and 2 varcodes
    var_codes_yr1=[]
    var_codes_yr2=[] #initialize with vars for total population and total housing units, which will be used to filter census tracts
    #'B03002_001E','B25034_001E'
    
    #loop through indices list
    for index in indices:
        
        if index == 'ding':
            for varcode in ding_vars:
                var_codes_yr1.append(varcode)
            for varcode in ding_vars:
                var_codes_yr2.append(varcode)
    
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
    df_list = []
    
    ##year 0##
    
    if len(years) > 2:
    
        if int(years[0]) == 2000:
            #assign census_df_yr0 to output of census_request_tract function for 2000 and var_codes_yr0
            census_df_yr0 = census_request_tract(years[0], state, county, var_codes_yr0)
            #assign tiger_df_yr0 to output of tiger_request for 2000
            tiger_df_yr0 = tiger_request(years[0], state, county)
            #merge and assign to df_yr0
            df_yr0 = tract_merge(census_df_yr0, tiger_df_yr0)
            #append df_year0 to df_list
            df_list.append(df_yr0)
        else:
            #assign acs_df_yr0 to output of acs_request_tract function for years[0] and var_codes_yr0
            acs_df_yr0 = acs_request_tract(years[0], state, county, var_codes_yr0)
            #assign tiger_df_yr0 to output of tiger_request for years[0]
            tiger_df_yr0 = tiger_request(years[0], state, county)
            #merge and assign to df_yr0
            df_yr0 = tract_merge(acs_df_yr0, tiger_df_yr0)
            #append df_year0 to df_list
            df_list.append(df_yr0)
   
    
   ##year 1##
    acs_df_yr1 = acs_request_tract(years[-2], state, county, var_codes_yr1) 
        #assign acs_df_yr1 to output of acs_request_tract function for years[1] and var_codes_yr1
    tiger_df_yr1 = tiger_request(years[-2], state, county)    
        #assign tiger_df_yr1 to output of tiger_request for years[1]
    df_yr1 = tract_merge(acs_df_yr1, tiger_df_yr1)
        #merge and assign to df_yr1
    df_list.append(df_yr1)
        #append df_yr1 to df_list
        
    ##year 2##
    acs_df_yr2 = acs_request_tract(years[-1], state, county, var_codes_yr2)  
        #assign acs_df_yr2 to output of acs_request_tract function for years[2] and var_codes_yr2
    tiger_df_yr2 = tiger_request(years[-1], state, county)   
        #assign tiger_df_yr2 to output of tiger_request for years[2]
    df_yr2 = tract_merge(acs_df_yr2, tiger_df_yr2)
        #merge and assign to df_yr2
    df_list.append(df_yr2)
        #append df_yr2 to df_list
        
    
    ###Harmonize dataframes to the tracts in year 2 and filter###

    target_df = df_list[-1]
    input_dfs = df_list[0:-1]
    
    # target_df = target_df.to_crs('ESRI:102008')
    # for input_df in input_dfs:
    #     input_df = input_df.to_crs('ESRI:102008')
    
    df = harmonize_tracts(target_df, input_dfs)
    
           
              
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
        
        if index == 'ding':
            for varcode in ding_vars_area:
                var_codes_yr1.append(varcode)
            for varcode in ding_vars_area:
                var_codes_yr2.append(varcode)

        
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
    df_yr1 = acs_request_area(years[-2], state, county, var_codes_yr1)
    #drop all columns except acs variables and add suffix _yr1
    
    #.add_suffix('_yr1')    
    df_yr1.add_suffix('_yr1')     
    
    for col in df_yr1.columns.to_list():
        df_yr1[col] = df_yr1[col].astype(int)
       
        
    ##year 2##
    df_yr2 = acs_request_area(years[-1], state, county, var_codes_yr2)
        #assign df_yr2 to output of acs_request_area function for years[2] and var_codes_yr2
    df_yr2.add_suffix('_yr2')
        #drop all columns except acs variables and GEOID and add suffix _yr2
        #.add_suffix('_yr2')
    for col in df_yr2.columns.to_list():
        df_yr2[col] = df_yr2[col].astype(int)
        
    df = pd.merge(df_yr1, df_yr2, left_index = True, right_index = True, suffixes=('_yr1', '_yr2'))   
        #merge two dfs by index  and assign to df
        
    return df    
            
#%%

###TEST###

# testdf = get_api_data_tract('42', '101', years = [2000, 2010, 2020], indices = ["ding", "bates"])

# testdf_area = get_api_data_county(42, 101, years = [2010,2020], indices = ["ding", "bates"])
            
            
            
            
            

