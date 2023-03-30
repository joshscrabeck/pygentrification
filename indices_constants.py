# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 22:35:24 2023

@author: tup13970
"""

##Constants 

ding_vars = ['B25064_001E', 'B25077_001E',
       'S1501_C01_001E', 'S1501_C01_006E',
       'S1501_C01_005E', 'S1501_C01_012E',
       'B19013_001E']

ding_vars_area = ['B25064_001E', 'B25077_001E', 'B19013_001E']

bates_vars_yr1 = ['B25003_001E', 'B25003_002E',  
              'B25003_003E', 'B03002_001E',  
              'B03002_003E', 'S1501_C01_001E', 
              'S1501_C01_006E',
              'S1501_C01_005E', 'S1501_C01_012E',
              'B19113_001E', 'B19013_001E', 
              'B25077_001E']

bates_vars_yr2 = ['B25003_001E', 'B25003_002E',  
              'B25003_003E', 'B03002_001E',  
              'B03002_003E', 'S1501_C01_001E', 
              'S1501_C01_006E',
              'S1501_C01_005E', 'S1501_C01_012E',
              'B19113_001E', 'B19013_001E', 
              'B25077_001E', 'B25034_001E', 
              'B25034_002E', 'B25034_003E',
              'B25034_004E']

bates_vars_census_yr0 = ['H085001']

bates_vars_acs_yr0 = ['B25077_001E']

bates_vars_area = ['B19013_001E','B19013_001M', 'B19113_001E', 'B19113_001M']

master_tract_dict = {'B25064_001E':'med_rent','H085001':'med_home_val', 'B25077_001E':'med_home_val', 'B25003_001E':'pop_tenure', 
              'B25003_002E': 'owner', 'B25003_003E': 'renter', 'B03002_001E':'pop_race', 'B03002_003E': 'white',
              'S1501_C01_001E':'pop_18_24', 'S1501_C01_006E':'pop_25_over',
              'S1501_C01_005E':'pop_18_24_edu', 'S1501_C01_012E':'pop_25_over_edu',
              'B19113_001E':'med_fam_inc', 'B19013_001E':'med_house_inc', 'B25034_001E':'tot_house', 'B25034_002E':'new_house_col1',
              'B25034_003E':'new_house_col2', 'B25034_004E':'new_house_col3'}

master_county_dict = {'B25064_001E':'area_med_rent', 'B25077_001E':'area_med_home_val',
                      'B19013_001E':'area_med_house_inc', 'B19013_001M':'area_med_house_inc_e', 
                      'B19113_001E':'area_med_fam_inc', 'B19113_001M':'area_med_fam_inc_e'}



##Includes all unique variables + single values for Bates-Freeman



