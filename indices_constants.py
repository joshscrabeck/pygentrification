# -*- coding: utf-8 -*-
"""
Constants needed for get_api_data_tract() and get_api_data_area()
"""

#Variables needed for Ding (2015) index at tract level fo year 1 and year 2
ding_vars = ['B25064_001E', 'B25077_001E',
       'B15002_002E', 'B15002_015E','B15002_016E', 'B15002_017E', 
       'B15002_018E', 'B15002_019E', 'B15002_032E', 'B15002_033E',
       'B15002_034E', 'B15002_035E', 'B19013_001E']

#Variables needed for Ding (2015) index at county level for year 1 and year 2
ding_vars_area = ['B25064_001E', 'B25077_001E', 'B19013_001E']

#Variables needed for Bates(2013) and Freeman (2005) indices at tract level for year 1
bates_vars_yr1 = ['B25003_001E', 'B25003_002E','B25003_003E', 'B03002_001E',
                  'B03002_003E', 'B15002_002E', 'B15002_015E','B15002_016E', 
                  'B15002_017E', 'B15002_018E', 'B15002_019E', 'B15002_032E',
                  'B15002_033E', 'B15002_034E', 'B15002_035E', 'B19113_001E', 
                  'B19013_001E', 'B25077_001E']

#Variables needed for Bates(2013) and Freeman (2005) indices at tract level for year 2
bates_vars_yr2 = ['B25003_001E', 'B25003_002E', 'B25003_003E', 'B03002_001E',  
                  'B03002_003E',  'B15002_002E', 'B15002_015E','B15002_016E',
                  'B15002_017E','B15002_018E', 'B15002_019E', 'B15002_032E', 
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
master_tract_dict = {'B25064_001E':'med_rent','H085001':'med_home_val', 'B25077_001E':'med_home_val', 'B25003_001E':'pop_tenure', 
              'B25003_002E': 'owner', 'B25003_003E': 'renter', 'B03002_001E':'pop_race', 'B03002_003E': 'white',  'B15002_002E': 'pop_25_over_m', 
              'B15002_015E': 'ba_degree_m','B15002_016E': 'ma_degree_m', 'B15002_017E': 'prof_degree_m', 'B15002_018E': 'doc_degree_m', 
              'B15002_019E': 'pop_25_over_f', 'B15002_032E': 'ba_degree_f', 'B15002_033E': 'ma_degree_f', 'B15002_034E': 'prof_degree_f', 
              'B15002_035E': 'doc_degree_f', 'B19113_001E':'med_fam_inc', 'B19013_001E':'med_house_inc', 'B25034_001E':'tot_house', 
              'B25034_002E':'new_house_col1', 'B25034_003E':'new_house_col2', 'B25034_004E':'new_house_col3'}

#dict for renaming columns for county-level variables 
master_county_dict = {'B25064_001E':'area_med_rent', 'B25077_001E':'area_med_home_val',
                      'B19013_001E':'area_med_house_inc', 'B19013_001M':'area_med_house_inc_e',
                      'B19113_001E':'area_med_fam_inc', 'B19113_001M':'area_med_fam_inc_e'}

#state dict
state_dict = {'01':'ALABAMA',       
'02':'ALASKA',
'04':'ARIZONA', 
'05':'ARKANSAS', 
'06':'CALIFORNIA', 
'08':'COLORADO', 
'09':'CONNECTICUT', 
'10':'DELAWARE',
'11':'DISTRICT_OF_COLUMBIA', 
'12':'FLORIDA',
'13':'GEORGIA', 
'15':'HAWAII',
'16':'IDAHO',
'17':'ILLINOIS', 
'18':'INDIANA', 
'19':'IOWA', 
'20':'KANSAS', 
'21':'KENTUCKY', 
'22':'LOUISIANA', 
'23':'MAINE', 
'24':'MARYLAND', 
'25':'MASSACHUSETTS', 
'26':'MICHIGAN', 
'27':'MINNESOTA', 
'28':'MISSISSIPPI', 
'29':'MISSOURI', 
'30':'MONTANA', 
'31':'NEBRASKA', 
'32':'NEVADA', 
'33':'NEW_HAMPSHIRE', 
'34':'NEW_JERSEY', 
'35':'NEW_MEXICO', 
'36':'NEW_YORK', 
'37':'NORTH_CAROLINA', 
'38':'NORTH_DAKOTA', 
'39':'OHIO', 
'40':'OKLAHOMA', 
'41':'OREGON', 
'42':'PENNSYLVANIA', 
'44':'RHODE_ISLAND', 
'45':'SOUTH_CAROLINA', 
'46':'SOUTH_DAKOTA', 
'47':'TENNESSEE', 
'48':'TEXAS', 
'49':'UTAH', 
'50':'VERMONT', 
'51':'VIRGINIA', 
'53':'WASHINGTON', 
'54':'WEST_VIRGINIA',
'55':'WISCONSIN', 
'56':'WYOMING', 
'60':'AMERICAN_SAMOA', 
'66':'GUAM', 
'69':'COMMONWEALTH_OF_THE_NORTHERN_MARIANA_ISLANDS',           
'72':'PUERTO_RICO',   
'78':'VIRGIN_ISLANDS_OF_THE_UNITED_STATES'}

state_dict_abr = {'01':'al',       
'02':'ak',
'04':'az', 
'05':'ar', 
'06':'ca', 
'08':'co', 
'09':'ct', 
'10':'de',
'11':'dc', 
'12':'fl',
'13':'ga', 
'15':'hi',
'16':'id',
'17':'il', 
'18':'in', 
'19':'ia', 
'20':'ks', 
'21':'ky', 
'22':'la', 
'23':'me', 
'24':'md', 
'25':'ma', 
'26':'mi', 
'27':'mn', 
'28':'ms', 
'29':'mo', 
'30':'mt', 
'31':'ne', 
'32':'nv', 
'33':'nh', 
'34':'nj', 
'35':'nm', 
'36':'ny', 
'37':'nc', 
'38':'nd', 
'39':'oh', 
'40':'ok', 
'41':'or', 
'42':'pa', 
'44':'ri', 
'45':'sc', 
'46':'sd', 
'47':'tn', 
'48':'tx', 
'49':'ut', 
'50':'vt', 
'51':'va', 
'53':'wa', 
'54':'wv',
'55':'wi', 
'56':'wy', 
'60':'as', 
'66':'gu', 
'69':'mp',           
'72':'pr',   
'78':'vi'}




