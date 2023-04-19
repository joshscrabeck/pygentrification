
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




