# -*- coding: utf-8 -*-

#%%
from io import BytesIO
import requests
import pandas as pd
import geopandas as gpd
#import json
from zipfile import ZipFile
import urllib
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas
import warnings
from tobler.area_weighted import area_interpolate
from functools import reduce

#%%

###Constants needed for acs and census api requests###


#Variables needed for Ding (2015) index at tract level fo year 1 and year 2
ding_vars = ['B01003_001E','B25064_001E', 'B25077_001E',
       'B15002_001E', 'B15002_015E','B15002_016E', 'B15002_017E', 
       'B15002_018E', 'B15002_032E', 'B15002_033E',
       'B15002_034E', 'B15002_035E', 'B19013_001E', 'B25034_001E']

#Variables needed for Ding (2015) index at county level for year 1 and year 2
ding_vars_area = ['B25064_001E', 'B25077_001E', 'B19013_001E']

#Variables needed for Bates(2013) and Freeman (2005) indices at tract level for year 1
bates_vars_yr1 = ['B25003_001E', 'B25003_002E','B25003_003E', 'B03002_001E',
                  'B03002_003E', 'B15002_001E', 'B15002_015E','B15002_016E', 
                  'B15002_017E', 'B15002_018E', 'B15002_032E',
                  'B15002_033E', 'B15002_034E', 'B15002_035E', 'B19113_001E', 
                  'B19013_001E', 'B25077_001E']

#Variables needed for Bates(2013) and Freeman (2005) indices at tract level for year 2
bates_vars_yr2 = ['B01003_001E','B25003_001E', 'B25003_002E', 'B25003_003E', 'B03002_001E',  
                  'B03002_003E',  'B15002_001E', 'B15002_015E','B15002_016E',
                  'B15002_017E','B15002_018E', 'B15002_032E', 
                  'B15002_033E', 'B15002_034E', 'B15002_035E', 'B19113_001E', 
                  'B19013_001E', 'B25077_001E', 'B25034_001E', 'B25034_002E', 
                  'B25034_003E', 'B25034_004E']

#Variable  needed for Bates(2013) home value index at tract level for year 0 (if year 0 is 2000)
bates_vars_census_yr0 = ['H085001']

#Variable  needed for Bates(2013) home value index at tract level for year 0 (if year 0 is not 2000)
bates_vars_acs_yr0 = ['B25077_001E']

#Variables needed for Bates(2013) and Freeman (2005) indices at county level for year 1
bates_vars_area_yr1 = ['B19013_001E','B19013_001M', 'B19113_001E', 'B19113_001M']

#Variables needed for Bates(2013) and Freeman (2005) indices at county level for year 2
bates_vars_area_yr2 = ['B19013_001E','B19013_001M', 'B19113_001E', 'B19113_001M']

#dict for renaming columns for tract-level variables 
master_tract_dict = {'B01003_001E':'tot_pop','B25064_001E':'med_rent','H085001':'med_home_val', 'B25077_001E':'med_home_val', 'B25003_001E':'pop_tenure', 
              'B25003_002E': 'owner', 'B25003_003E': 'renter', 'B03002_001E':'pop_race', 'B03002_003E': 'white',  'B15002_001E': 'pop_25_over', 
              'B15002_015E': 'ba_degree_m','B15002_016E': 'ma_degree_m', 'B15002_017E': 'prof_degree_m', 'B15002_018E': 'doc_degree_m', 
              'B15002_032E': 'ba_degree_f', 'B15002_033E': 'ma_degree_f', 'B15002_034E': 'prof_degree_f', 
              'B15002_035E': 'doc_degree_f', 'B19113_001E':'med_fam_inc', 'B19013_001E':'med_house_inc', 'B25034_001E':'tot_house', 
              'B25034_002E':'new_house_col1', 'B25034_003E':'new_house_col2', 'B25034_004E':'new_house_col3'}

#dict for renaming columns for county-level variables 
master_county_dict = {'B25064_001E':'area_med_rent', 'B25077_001E':'area_med_home_val',
                      'B19013_001E':'area_med_house_inc', 'B19013_001M':'area_med_house_inc_e',
                      'B19113_001E':'area_med_fam_inc', 'B19113_001M':'area_med_fam_inc_e'}

#%%
##harmonization function##
def harmonize_tracts(target_df, input_dfs = []):
    ''' This function takes in a target GeoDataFrame and a list of input GeoDataFrames. The target_df has the target geometry and the function uses the tobler package's areal interpolation
    function to harmonize the data in each input GeoDataFrame with the geometry in the target dataframe. 
    
    Parameters
    -------------
    target_df: GeoDataFrame with target geometry
    input_dfs: List of GeoDataFrames 

    Returns
    ------------
    GeoDataFrame
    
    This function will return a single GeoDataFrame with all interpolated columns from all input dfs and the geometry and all original columns from the target df. 
    The interpolated columns will have suffixes corresponding to their order in the input_dfs parameter. If there is more than one input df (for year o - year n), the suffix will start at '_yr0' and the target_df will have teh suffix '_yr{n}'. If there is only one input df the suffix will be '_yr1' and the target_df will have suffix '_yr2'.
    
    References
    -------------
    https://github.com/pysal/tobler
    
    Notes
    -------------
    This function uses lists of possible extensive variables and intensive variables, which together include all possible column names needed to calculate the gentrification indices in this package.
    
      '''

    
    #define lists with all possible intensive and extensive variables
    all_extensive_vars = ['tot_pop','pop_tenure', 'owner', 'renter', 'pop_25_over', 'ba_degree_m', 'ma_degree_m', 'prof_degree_m', 'doc_degree_m', 'ba_degree_f', 'ma_degree_f', 'prof_degree_f', 'doc_degree_f',  'pop_race', 'white', 'tot_house', 'new_house_col1', 'new_house_col2', 'new_house_col3']
    all_intensive_vars = ['med_rent','med_fam_inc', 'med_home_val', 'med_house_inc']
    
    #take in list of input dfs and make two lists of lists - one for extensive and one for intensive
    extensive_variables = []
    intensive_variables = []
    
    for input_df in input_dfs:
        e_vars = []
        i_vars = []
        col_list = input_df.columns.to_list()
        for col in col_list:
            if col in all_extensive_vars:
                e_vars.append(col)
            elif col in all_intensive_vars:
                i_vars.append(col)
        if len(e_vars) > 0:
            extensive_variables.append(e_vars)
        else:
            extensive_variables.append(None)
        if len(i_vars) > 0:
            intensive_variables.append(i_vars)

        else:
            intensive_variables.append(None)
    
    #initialize vars for areal interpolation loop
    if len(input_dfs) == 1:
        i = 1
    
    elif len(input_dfs) > 1:
        i = 0
    
    varslist = 0
    merge_dfs = []
    
    #use tobler's areal interpolation function and add output dfs to list
    for input_df in input_dfs:    
        interpolated_columns = area_interpolate(input_df, target_df, extensive_variables = extensive_variables[varslist], intensive_variables= intensive_variables[varslist])
        interpolated_columns.drop(['geometry'], axis = 1, inplace = True)
        interpolated_columns = interpolated_columns.add_suffix(f'_yr{i}')
        interpolated_columns = interpolated_columns.reset_index(drop = True)
        merge_dfs.append(interpolated_columns)
        i += 1
        varslist += 1
       
    #add suffix to target df, rename columns, and reset index
    target_df = target_df.add_suffix(f'_yr{i}')
    target_df = target_df.rename(columns = {f'geometry_yr{i}': 'geometry', f'GEOID_yr{i}': 'GEOID'})
    target_df = target_df.set_geometry('geometry')
    target_df = target_df.reset_index(drop = True)
    #merge_dfs.append(target_df)
    
    df_list = [target_df]
    for df in merge_dfs:
        df_list.append(df)
    
    #merge output dfs from aerial interpolation with target df
    output = reduce(lambda left,right: left.merge(right, left_index = True, right_index = True, how='inner'), df_list)
    

    return output


#%%

###api request base functions###
def acs_request_tract(year, state, county, req_vars):
    
    ''' 
    This function retrives data from the Census, 5 year 
    American Community Survey. Each tract within the state and county will be 
    retrieved according to the index and variables requested. 
    
    Parameters
    ----------------
    year: int or string
    state: int or string 
        FIPS State Numeric Code
    county: int or string 
        FIPS County Numeric Code
    req_vars: list
        variables being requested from the Census API related to the requested index
    
    Returns
    ----------------
    DataFrame
    
    '''
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    #print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(req_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
    #predicates["key"] = ____________________
    r = requests.get(acs_base_url, params=predicates)
    j = r.json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict)
    df['GEOID'] = df['state']+df['county']+df['tract']
    df = df.drop(columns = ['state', 'county', 'tract'])
    df = df.apply(pd.to_numeric, errors = 'coerce')
    df[df<0] = 0
    return df

def acs_request_area(year, state, county, req_vars):
    ''' 
    This function retrives data from the Census, 5 year 
    American Community Survey. This function specifically requests variables
    for the entire study area as a whole, rather than individual census tracts.
    
    Parameters
    ----------------
    year: int or string
    state: int or string 
        FIPS State Numeric Code
    county: int or string 
        FIPS County Numeric Code
    req_vars: list
        variables being requested from the Census API related to the requested index (string)
    
    Returns
    ----------------
    DataFrame
    
    '''
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "acs/acs5"
    acs_base_url = "/".join([HOST, year, dataset])
    #print(acs_base_url)
    predicates = {}
    predicates["get"] = ",".join(req_vars)
    predicates["for"] = f"county:{county}"
    predicates["in"] = f"state:{state}"
    #predicates["key"] = ____________________
    j = requests.get(acs_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_county_dict)
    df = df.apply(pd.to_numeric, errors = 'coerce')
    df[df<0] = 0
    return df


def census_request_tract(year, state, county, req_vars):
    ''' 
    This function retrives data from the Decennial Census. Each tract within 
    the state and county will be retrieved according to the index and variables 
    requested. 
    
    Parameters
    ----------------
    year: int or string
    state: int or string 
        FIPS State Numeric Code
    county: int or string 
        FIPS County Numeric Code
    req_vars: list
        variables being requested from the Census API related to the requested index

    Returns
    ----------------
    DataFrame
    
    '''
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dec/sf3?"
    census_base_url = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(req_vars)
    predicates["for"] = "tract:*"
    predicates["in"] = f"state:{state}, county:{county}"
    j = requests.get(census_base_url, params=predicates).json()
    df = pd.DataFrame(data=j[1:], columns=j[0]).rename(columns = master_tract_dict)
    df['GEOID'] = df['state']+df['county']+df['tract']
    df = df.drop(columns = ['state', 'county', 'tract'])
    df = df.apply(pd.to_numeric, errors = 'coerce')
    df[df<0] = 0
    return df

def tiger_request(year, state, county):
    ''' 
    This function retrives data from the Decennial Census, specifically the
    geometry. Each tract within the state and county will be 
    retrieved. 
    
    Parameters
    ----------------
    year: int or string
    state: int or string
        FIPS State Numeric Code 
    county: int or string
        FIPS County Numeric Code
    
    Returns
    ----------------
    GeoDataFrame
    
    '''
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
    ''' 
    This function merges the dataframes from above requests to create one 
    dataframe to be analzyed by the index calculations. 
    
    Parameters
    ----------------
    acs_df: df
        ACS request dataframe with variable information, state, and county information. 
    t_df: gdf
        tiger request dataframe with tract geometry
    
    Returns
    ----------------
    GeoDataFrame
    
    '''
    acs_df = acs_df.drop(columns = ['GEOID'])
    gdf = t_df.merge(acs_df, left_index = True, right_index =  True)

    return gdf

#%%

###comprehensive api call function for tract-level###

def get_api_data_tract(state, county, years, indices, proj_crs = 'EPSG:4269'):
    
    ''' 
    This function retrives data from the Census, 5 year 
    American Community Survey. Each tract within the state and county will be 
    retrieved according to the index and variables requested. 
    
    Parameters
    ----------------
    state: string
        FIPS State Numeric Cod
    county: string 
        FIPS County Numeric Code
    years: list
        years for api calls. "bates" requires 3 years, ding only requires 2.
    indices: list
        List of strings that pecify the index or indices for the correct variables to be 
        retrieved. Acceptable arguments include "bates" and "ding".
    proj_crs: string
        EPSG for protected coordinate reference system for study area in 'EPSG: XXXX' format
    
    Returns
    ----------------
    GeoDataFrame
    
    
    '''
     
    ###check input###
    
    ##CRS##
    
    if proj_crs == 'EPSG:4269':
        warnings.warn("The default coordinate reference system for this function is EPSG 4269, which is a geographic crs and may lead to inaccurate areal interpolation. For the most accurate data, please set the crs parameter to a projected crs that is appropriate for your study area.")
    
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
    var_codes_yr2=[]
    
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
            #assign tiger_df_yr0 to output of tiger_request for 2000 and set crs
            tiger_df_yr0 = tiger_request(years[0], state, county).to_crs(crs = proj_crs)
            #merge and assign to df_yr0
            df_yr0 = tract_merge(census_df_yr0, tiger_df_yr0)
            #append df_year0 to df_list
            df_list.append(df_yr0)
        else:
            #assign acs_df_yr0 to output of acs_request_tract function for years[0] and var_codes_yr0
            acs_df_yr0 = acs_request_tract(years[0], state, county, var_codes_yr0)
            #assign tiger_df_yr0 to output of tiger_request for years[0] and set crs
            tiger_df_yr0 = tiger_request(years[0], state, county).to_crs(crs = proj_crs)
            #merge and assign to df_yr0
            df_yr0 = tract_merge(acs_df_yr0, tiger_df_yr0)
            #append df_year0 to df_list
            df_list.append(df_yr0)
   
    
   ##year 1##
    #assign acs_df_yr1 to output of acs_request_tract function for years[1] and var_codes_yr1
    acs_df_yr1 = acs_request_tract(years[-2], state, county, var_codes_yr1) 
    #assign tiger_df_yr1 to output of tiger_request for years[1] and set crs
    tiger_df_yr1 = tiger_request(years[-2], state, county).to_crs(crs = proj_crs)    
    #merge and assign to df_yr1
    df_yr1 = tract_merge(acs_df_yr1, tiger_df_yr1)
    #append df_yr1 to df_list
    df_list.append(df_yr1)
        
    ##year 2##
    #assign acs_df_yr2 to output of acs_request_tract function for years[2] and var_codes_yr2
    acs_df_yr2 = acs_request_tract(years[-1], state, county, var_codes_yr2)  
    #assign tiger_df_yr2 to output of tiger_request for years[2] and set crs
    tiger_df_yr2 = tiger_request(years[-1], state, county).to_crs(crs = proj_crs)
    #merge and assign to df_yr2
    df_yr2 = tract_merge(acs_df_yr2, tiger_df_yr2)    
    #append df_yr2 to df_list
    df_list.append(df_yr2)
        
    
    ###Harmonize dataframes to the tracts in year 2###

    target_df = df_list[-1]
    input_dfs = df_list[0:-1]
    
    df = harmonize_tracts(target_df, input_dfs)
    
    df = df.to_crs('EPSG:4269')
           
    return df

#%%
    
###comprehensive api call function for county-level###

def get_api_data_county(state, county, years, indices):
    '''  
    This function retrives data from the Census, 5 year American Community 
    Survey. This function specifically requests variables for the entire study 
    area as a whole, rather than individual census tracts.
      
    Parameters
    ----------------
    state: int or string
        FIPS State Numeric Code
    county: int or string
        FIPS County Numeric Cod
    years: list
    indices: list
        specify the index or indices for the correct variables to be  retrieved.
    
    Returns
    ----------------
    DataFrame
      
    '''
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
    
    #loop through indices list and add vars to list
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
    
    #.add_suffix('_yr1')    
    df_yr1.add_suffix('_yr1')     
    
    for col in df_yr1.columns.to_list():
        df_yr1[col] = df_yr1[col].astype(int)
       
        
    ##year 2##
    #assign df_yr2 to output of acs_request_area function for years[2] and var_codes_yr2
    df_yr2 = acs_request_area(years[-1], state, county, var_codes_yr2)
    #.add_suffix('_yr2')
    df_yr2.add_suffix('_yr2')

    for col in df_yr2.columns.to_list():
        df_yr2[col] = df_yr2[col].astype(int)
        
    #merge two dfs by index  and assign to df
    df = pd.merge(df_yr1, df_yr2, left_index = True, right_index = True, suffixes=('_yr1', '_yr2'))   
        
        
    return df    
            
            
            

