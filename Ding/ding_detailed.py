#Simple binary result Ding method for gentrification indentification

#%%

import pandas as pd
import os
import numpy as np
import requests



os.getcwd()
os.chdir('.\documents\gus_8066\gentrification-indices\ding')

df = pd.read_csv('ding_df.csv')

#%% The Ding function, more detailed version, starts with defining nested census api calls

def ding_calc( yr1, yr2, study_area, inplace = False):
    
    tract_vars_name = ['census_tract', 'med_rent', 'med_home_val',
                 '18_24_pop', '25_over_pop',
                 '18_24_edu_pop', '25_over_edu_pop',
                 'med_hhi']

    area_vars_name = ['county', 'area_med_rent', 'area_med_home_val', 'area_med_hhi']
   
   
   def acs_req_tract(year):
       
       host = "https://api.census.gov/data"
       dataset = "acs/acs5"
       acs_base_url = "/".join(host, year, dataset)
       
       tract_vars = ['TRACT', 'B25064_001E', 'B25077_001E',
              'S1501_C01_001E', 'S1501_C01_006E',
              'S1501_C01_005E', 'S1501_C01_012E',
              'B25119_001E']
       
       
       predicates = {}
       predicates["get"] = ",".join(tract_vars)
       predicates["for"] = "tract:*"
       predicates["in"] = "state:42, county:101"
       #predicates["key"] = ____________________
       res = requests.get(acs_base_url, params=predicates)
       return res.text
       
# run acs tract function twice for the two user inputted years in the enclosing ding func
# and merge
     
   res_1 = acs_req_tract(yr1)
   data_1 = res_1.json()
   df_tract_1 = pd.DataFrame(data = data_1[1:], columns = tract_vars_name )
   
   res_2 = acs_req_tract(yr2)
   data_2 = res_2.json()
   df_tract_2 = pd.DataFrame(data = data_2[1:], columns = tract_vars_name) 
   
   df = pd.Merge(df_tract_1, df_tract_2, on = 'census_tract', suffix = ('_1', '_2'))
   
#  After tract level information for both ends of study period is present and merged
#  time to do the same for study area-wide figures.

   def acs_req_area(year):
       
      host = "https://api.census.gov/data"
      dataset = "acs/acs5"
      acs_base_url = "/".join(host, year, dataset)
      
      area_vars = ['COUNTY', 'B25064_001E', 'B25077_001E',
             'B25119_001E']
      
       predicates = {}
       predicates["get"] = ",".join(tract_vars)
       predicates["for"] = "county:*"
       predicates["in"] = "state:42, county:101"
       #predicates["key"] = ____________________
       res = requests.get(acs_base_url, params=predicates)
       return res.text
   
   area_res_1 = asc_req_area(yr1)
   area_data_1 = area_res_1.json()
   df_area_1 = pd.DataFrame(data = area_data_1[1:], columns = area_vars_name)
   
   area_res_2 = acs_req_area(yr2)
   area_data_2 = area_res_2.json()
   df_area_2 = pd.DataFrame(data = area_data_2[1:], columns = area_vars_name)
   
   area_df = pd.Merge(df_area_1, df_area_2, on = 'county', suffix = ('_1', '_2'))
       
       
       
# housekeeping

   copy_df = df.copy(deep = True)
    
   df = df.replace("-", np.nan)
   df = df.replace(",", "", regex= True)
   df = df.replace("2000+", "2000")
   df.iloc[:,2:] = df.iloc[:, 2:].astype('float')
    
# Creating figures of total adult & adult educated population
    
    
   df['pop_1'] = df['18_24_pop_1'] + df['25_over_pop_1'] 
   df['pop_2'] = df['18_24_pop_2'] + df['25_over_pop_2']
    
   df['edu_pop_1'] = df['18_24_edu_pop_1'] + df['25_over_edu_pop_1']
   df['edu_pop_2'] = df['18_24_edu_pop_2'] + df['25_over_edu_pop_2']
    
    
    
    
# Deriving change in share of college educated residents
    
    df['edu_perc_1'] = (df['edu_pop_1'] / df['pop_1'])*100
    df['edu_perc_2'] = (df['edu_pop_2'] / df['pop_2'])*100
    chg_edu_share = df['edu_perc_2'] - df['edu_perc_1']
    
# deriving changes in median rents and home values per tract
    
    chg_med_home_val = ((df['med_home_val_2'] - df['med_home_val_1']) / df['med_home_val_2'])*100
    chg_med_rent = ((df['med_rent_2'] - df['med_rent_1']) / df['med_rent_2'])*100
    
#  city wide figures
    
    area_pop_1 = df['pop_1'].sum()
    area_edu_pop_1 = df['edu_pop_1'].sum()
    area_edu_share_1 = (area_edu_pop_1 / area_pop_1)*100
    
    area_pop_2 = df['pop_2'].sum()
    area_edu_pop_2 = df['edu_pop_2'].sum()
    area_edu_share_2 = (area_edu_pop_2 / area_pop_2)*100
    
    area_chg_edu_share = area_edu_share_2 - area_edu_share_1
    
  
    area_home_val_perc_inc = ((area_df['area_med_home_val_2'] - area_df['area_med_home_val_1'])/ area_df['area_med_home_val_2'])*100
    area_med_rent_perc_inc = ((area_df['area_med_rent_2'] - area_df['area_med_rent_1'])/ area_df['area_med_rent_2'])*100
    
    #% Calculating ding index and creating a resulting dataframe with the tracts meeting the criteria
    
    df['gentrifiable'] = np.where(df['med_hhi_1'] < area_df['area_med_hhi_1'], True, False)
    
    df['hhi_crit'] = np.where((df['gentrifiable'] == True) & (df['pop_1'] > 50), 1, 0)
    
    df['rent_crit'] = np.where((chg_med_rent > area_med_rent_perc_inc) & (df['pop_1'] > 50), .5, 0)
    
    df['val_crit'] = np.where((chg_med_home_val > area_home_val_perc_inc) & (df['pop_1'] > 50), .5, 0)
    
    df['edu_crit'] = np.where((chg_edu_share > area_chg_edu_share) & (df['pop_1'] > 50), 1, 0)
    
    
    df['crit'] = df['hhi_crit'] + df['rent_crit'] + df['val_crit'] + df['edu_crit']
    
    df['gentrifying'] = np.where(df['crit'] >= 2.5, True, False)
    
    #%%
    
    gent_only_df = df[df['gentrifying'] == True]
    
    quant_rent_vals = np.quantile(gent_only_df['med_rent_2'], [0, 0.25, 0.50, 0.75, 1])
    
    quant_home_vals = np.quantile(gent_only_df['med_home_val_2'], [0, 0.25, 0.50, 0.75, 1])
    
    conditions = [
        df['gentrifying'] == True & df['med_rent_2'] <= quant_rent_vals[1] & df['med_home_val_2'] <= quant_home_vals[1],
        df['gentrifying'] == True & (df['med_rent_2'] <= quant_rent_vals[3] or df['med_home_vals_2'] <= quant_home_vals[3]),
        df['gentrifying'] == True & (df['med_rent_2'] > quant_rent_vals[3] or df['med_home_vals_2'] > quant_home_vals[3]),
        df['gentrifiable'] == True & df['gentrifying'] == False,
        df['gentrifiable'] == False
        ]
    
    choices = [
        'Weak Gentrification',
        'Moderate Gentrification',
        'Intense Gentrification',
        'No Gentrification',
        'Nongentrifiable'
        ]
    
    df['gent_status'] = np.select(conditions, choices)
    
    
    
    
    
    new_cols = df[['census_tract''hhi_crit', 'rent_crit', 'val_crit', 'edu_crit', 'crit', 'gent_status']].reset_index()
    
    keep_cols = df[['census_tract', 'med_rent_1', 'med_home_val_1',
                    '18_24_pop_1', '25_over_pop_1',
                    '18_24_edu_pop_1', '25_over_edu_pop_1',
                    'med_hhi_1','med_rent_2', 
                    'med_home_val_2','18_24_pop_2', 
                    '25_over_pop_2','18_24_edu_pop_2', 
                    '25_over_edu_pop_2']].reset_index()
    
    if inplace == False:
        output = pd.merge(keep_cols, new_cols, on= 'census_tract')
    
    else:
        output = pd.merge(copy_df, new_cols, on = 'census_tract')
    
    return output



