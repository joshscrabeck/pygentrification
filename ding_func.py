# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:22:03 2023

@author: tul54884
"""


# -*- coding: utf-8 -*-
# A calculation of the Ding (2015) gentrification index, using sample data from 

#%%

import pandas as pd
import os
import numpy as np


os.getcwd()
os.chdir('.\documents\gus_8066\gentrification-indices\ding')

df = pd.read_csv('ding_df.csv')

#%% Creating columns, data for calculation

def ding_calc(df, inplace = False):   #def ding_calc(df, yr1, yr2, study_area, inplace = False)

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
    
    
    
    
    #Deriving change in share of college educated residents
    
    df['edu_perc_1'] = (df['edu_pop_1'] / df['pop_1'])*100
    df['edu_perc_2'] = (df['edu_pop_2'] / df['pop_2'])*100
    chg_edu_share = df['edu_perc_2'] - df['edu_perc_1']
    
    #deriving changes in median rents and home values per tract
    
    chg_med_home_val = ((df['med_home_val_2'] - df['med_home_val_1']) / df['med_home_val_2'])*100
    chg_med_rent = ((df['med_rent_2'] - df['med_rent_1']) / df['med_rent_2'])*100
    
    #%  city wide figures
    
    area_pop_1 = df['pop_1'].sum()
    area_edu_pop_1 = df['edu_pop_1'].sum()
    area_edu_share_1 = (area_edu_pop_1 / area_pop_1)*100
    
    area_pop_2 = df['pop_2'].sum()
    area_edu_pop_2 = df['edu_pop_2'].sum()
    area_edu_share_2 = (area_edu_pop_2 / area_pop_2)*100
    
    area_chg_edu_share = area_edu_share_2 - area_edu_share_1
    
    area_med_hhi_1 = 34400
    #area_med_hhi_2 = 49127
    area_med_rent_1 = 819
    area_med_rent_2 = 1084
    area_med_home_val_1 = 135200
    area_med_home_val_2 = 171600
    
    area_home_val_perc_inc = ((area_med_home_val_2 - area_med_home_val_1)/ area_med_home_val_2)*100
    area_med_rent_perc_inc = ((area_med_rent_2 - area_med_rent_1)/ area_med_rent_2)*100
    
    #% Calculating ding index and creating a resulting dataframe with the tracts meeting the criteria
    
    
    
    df['hhi_crit'] = np.where((df['med_hhi_1'] < area_med_hhi_1) & (df['pop_1'] > 50), 1, 0)
    
    df['rent_crit'] = np.where((chg_med_rent > area_med_rent_perc_inc) & (df['pop_1'] > 50), .5, 0)
    
    df['val_crit'] = np.where((chg_med_home_val > area_home_val_perc_inc) & (df['pop_1'] > 50), .5, 0)
    
    df['edu_crit'] = np.where((chg_edu_share > area_chg_edu_share) & (df['pop_1'] > 50), 1, 0)
    
    
    df['crit'] = df['hhi_crit'] + df['rent_crit'] + df['val_crit'] + df['edu_crit']
    
    df['gent_status'] = np.where(df['crit'] >= 2.5, True, False)
    
    #
    
    new_cols = df[['hhi_crit', 'rent_crit', 'val_crit', 'edu_crit', 'crit', 'gent_status']].reset_index()
    
    keep_cols = df[['census_tract', 'med_rent_1', 'med_home_val_1',
                    '18_24_pop_1', '25_over_pop_1',
                    '18_24_edu_pop_1', '25_over_edu_pop_1',
                    'med_hhi_1','med_rent_2', 
                    'med_home_val_2','18_24_pop_2', 
                    '25_over_pop_2','18_24_edu_pop_2', 
                    '25_over_edu_pop_2']].reset_index()
    
    if inplace == False:
        output = pd.merge(keep_cols, new_cols, left_index = True, right_index = True)
    
    else:
        output = pd.merge(copy_df, new_cols, left_index = True, right_index = True)
    
    return output



