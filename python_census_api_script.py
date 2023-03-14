#!/usr/bin/env python
# coding: utf-8

# In[3]:

#HUD CHAS API Token
##eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMyZmNmNzI5NDg5NzZkMmUyNjM4MWM1ZGUxNDMyYjIwZTBjM2ViNGYxMGJiN2IzZWU2NWFiOWQ0YTIzNWFhYjI5MTRjM2MzNTNiNTYzY2ZjIn0.eyJhdWQiOiI2IiwianRpIjoiMzJmY2Y3Mjk0ODk3NmQyZTI2MzgxYzVkZTE0MzJiMjBlMGMzZWI0ZjEwYmI3YjNlZTY1YWI5ZDRhMjM1YWFiMjkxNGMzYzM1M2I1NjNjZmMiLCJpYXQiOjE2NzY5NDUyMDIsIm5iZiI6MTY3Njk0NTIwMiwiZXhwIjoxOTkyNTY0NDAyLCJzdWIiOiI0NzI2MSIsInNjb3BlcyI6W119.KXmlEzT08PT4mnJjYLNPhdGSFgDS-LYlpZn5ZpTjuN0lZFBM9ixZA0V1wlpcx99aIVSR3K6Cc2ixsT4ryXUsAA

import os
import requests
import numpy
import pandas as pd
import json
from pprint import pprint


HOST = "https://api.census.gov/data"
year = "2020"
dataset = "acs/acs5"
acs_base_url = "/".join([HOST, year, dataset])

print(acs_base_url)

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

HOST = "https://api.census.gov/data"
year = "1990"
dataset = "dicennial/dicennial"
census_base_url_1990 = "/".join([HOST, year, dataset])

print(census_base_url_1990)

# In[5]:


# Build the list of variables to request
get_vars_bates_vuln = ['B25003_001E', 'B25003_001M', 
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
                       'B25034_003E', 'B25034_003M']

bates_vuln_col_names = ['pop_ten','pop_ten_e', 'owner', 'owner_e', 'renter', 'renter_e',
                        'poprac', 'poprac_e', 'white', 'white_e', 'popedu', 'popedu_e',
                        'popedum', 'popedum_e', 'ASdegm', 'ASdegm_e', 'BAdegm', 'BAdegm_e', 
                        'MAdegm', 'MAdegm_e', 'prodegm', 'prodegm_e', 'drdegm',
                        'drdegme', 'popeduf', 'popeduf_e', 'ASdegf', 'ASdegf_e',
                        'BAdegf', 'BAdegf_e', 'MAdegf', 'MAdegf_e', 'prodegf',
                        'prodegf_e', 'drdegf', 'drdegf_e', 'mfi', 'mfi_e', 'mhi', 'mhi_e',
                        'mhv', 'mhv_e', 'tothous', 'tothous_e', 'y14topr', 'y14topr_e',
                        'y10to13', 'y10to13_e', 'state', 'county', 'tract']


get_renter = ["B25008_001E", "B25008_003E"]
print(get_vars_bates_vuln)
print(get_renter)


# In[6]:


def census_acs_req():
    predicates = {}
    predicates["get"] = ",".join(get_vars_bates_vuln)
    predicates["for"] = "tract:*"
    predicates["in"] = "state:42, county:101"
    #predicates["key"] = ____________________
    r = requests.get(acs_base_url, params=predicates)
    return r.text

#use geosnap for 1990-2010, tiger census for 2020 geometries.
#harmonize.harmonize(gdf[, target_year, ...]) ,
#Use spatial interpolation to standardize neighborhood boundaries over time.

r = census_acs_req()
print(r)
print(r.json())

json_response = r
print(json_response)
res = json.loads(json_response)
print(res)

vuln_df = pd.DataFrame(columns=bates_vuln_col_names, data=res[1:])


print(vuln_df.head())
# In[12]:


# Fix columns that should be numeric
vuln_df["mhi"] = vuln_df["mhi"].astype(int)
# In[13]:

HOST = "https://api.census.gov/data"
year = "2010"
dataset = "acs/acs5"
acs_base_url_2010 = "/".join([HOST, year, dataset])


HOST = "https://api.census.gov/data"
year = "2000"
dataset = "dec"
census_base_url_2000 = "/".join([HOST, year, dataset])
print(census_base_url_2000)


# In[14]:

get_vars_bates_vuln = ['B25003_001E', 'B25003_001M', 
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
                       'B19113_001E', 'B19113_001M']

bates_vuln_col_names = ['pop_tenure','pop_tenure_e', 'owners', 'owners_e', 'renters', 'renters_e',
                        'pop_race', 'pop_race_e', 'white_nhl', 'white_nhl_e', 'pop_edu', 'pop_edu_e',
                        'pop_edu_m', 'pop_edu_m_e', 'ASdegree_m', 'ASdegree_m_e', 'BAdegree_m', 'BAdegree_m_e', 
                        'MAdegree_m', 'MAdegree_m_e', 'profdegree_m', 'profdegree_m_e', 'docdegree_m',
                        'docdegree_m_e', 'pop_edu_f', 'pop_edu_f_e', 'ASdegree_f', 'ASdegree_f_e',
                        'BAdegree_f', 'BAdegree_f_e', 'MAdegree_f', 'MAdegree_f_e', 'profdegree_f',
                        'profdegree_f_e', 'docdegree_f', 'docdegree_f_e', 'mfi', 'mfi_e', 'state', 
                        'county', 'tract',]

# In[15]

def census_acs_req_2010_acs():
    predicates = {}
    predicates["get"] = ",".join(get_vars_bates_vuln)
    predicates["for"] = "tract:*"
    predicates["in"] = "state:42, county:101"
    #predicates["key"] = ____________________
    r = requests.get(acs_base_url_2010, params=predicates)
    return r.text

r_2010 = census_acs_req_2010_acs()
print(r_2010)
print(r_2010.json())

json_response = r_2010
print(json_response)
res = json.loads(json_response)
print(res)

vuln_df_2010 = pd.DataFrame(columns=bates_vuln_col_names, data=res[1:])
print(vuln_df_2010.head())

def census_acs_req_2000():
    predicates = {}
    predicates["get"] = ",".join(get_vars_bates_vuln)
    predicates["for"] = "tract:*"
    predicates["in"] = "state:42, county:101"
    #predicates["key"] = ____________________
    r = requests.get(census_base_url_2000, params=predicates)
    return r.text

r_2000 = census_acs_req_2000()
print(r_2000)
print(r_2000.json())

json_response = r_2000
print(json_response)
res = json.loads(json_response)
print(res)

vuln_df_2000 = pd.DataFrame(columns=bates_vuln_col_names, data=res[1:])
print(vuln_df_2000.head())

merged_df = pd.merge(vuln_df_2010, vuln_df, on='state')
print(merged_df.tail())

os.makedirs('C:/Users/tup13970/Documents/GUS8066', exist_ok=True)
merged_df.to_csv('C:/Users/tup13970/Documents/GUS8066/out.csv')  


