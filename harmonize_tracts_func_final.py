

import pandas as pd
import os
from tobler.area_weighted import area_interpolate
import geopandas as gpd
from functools import reduce


os.chdir('/Users/wc555/gus8066/gentrification-indices/bates-freeman-data')

#%%

##Create test dfs##

#Import ACS_2020_tenure.csv and ACS_2010_tenure.csv
acs_2020_tenure = pd.read_csv('ACS_2020_tenure.csv', skiprows= [1]) #skip row with column descriptions
acs_2010_tenure = pd.read_csv('ACS_2010_tenure.csv', skiprows= [1]) 
shp10 = gpd.read_file('/Users/wc555/gus8066/tl_2010_42101_tract10.shp').to_crs('epsg:6565')
shp20 = gpd.read_file('tl_2022_42_tract.shp').to_crs('epsg:6565')
shp20 = shp20[shp20['COUNTYFP'] == '101']

#Rename relevant columns and drop unecessary columns
acs_2020_tenure = acs_2020_tenure.rename(columns = {'B25003_001E': 'pop_tenure', 'B25003_001M':'popten_e', 'B25003_002E': 'owners', 'B25003_002M':'owner_e', 'B25003_003E': 'renters', 'B25003_003M':'renter_e'})
acs_2020_tenure.dropna(axis='columns', inplace = True)
acs_2020_tenure = acs_2020_tenure[['GEO_ID', 'NAME', 'pop_tenure', 'owners', 'renters']]
acs_2020_tenure['GEO_ID'] = acs_2020_tenure['GEO_ID'].apply(lambda x: x[-11:])
shp_merge_2020 = shp20.merge(acs_2020_tenure, left_on = 'GEOID', right_on = 'GEO_ID', suffixes = ('_x', '_y'))


acs_2010_tenure = acs_2010_tenure.rename(columns = {'B25003_001E': 'pop_tenure', 'B25003_001M':'popten_e', 'B25003_002E': 'owners', 'B25003_002M':'owner_e', 'B25003_003E': 'renters', 'B25003_003M':'renter_e'})
acs_2010_tenure.dropna(axis='columns', inplace = True)
acs_2010_tenure = acs_2010_tenure[['GEO_ID', 'NAME', 'pop_tenure', 'owners', 'renters']]
acs_2010_tenure['GEO_ID'] = acs_2010_tenure['GEO_ID'].apply(lambda x: x[-11:])
shp_merge_2010 = shp10.merge(acs_2010_tenure, left_on = 'GEOID10', right_on = 'GEO_ID', suffixes = ('_x', '_y'))


#%%

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
    all_extensive_vars = ['pop_tenure', 'owner', 'renter', 'pop_18_24', 'pop_25_over', 'pop_18_24_edu', 'pop_25_over_edu', 'pop_race', 'white', 'tot_house', 'new_house_col1', 'new_house_col2', 'new_house_col3']
    all_intensive_vars = ['med_fam_inc', 'med_home_val', 'med_house_inc']
    
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
    
    
    if len(input_dfs) == 1:
        i = 1
    
    elif len(input_dfs) > 1:
        i = 0
    
    varslist = 0
    merge_dfs = []
    
    for input_df in input_dfs:    
        interpolated_columns = area_interpolate(input_df, target_df, extensive_variables = extensive_variables[varslist], intensive_variables= intensive_variables[varslist])
        interpolated_columns.drop(['geometry'], axis = 1, inplace = True)
        interpolated_columns = interpolated_columns.add_suffix(f'_yr{i}')
        merge_dfs.append(interpolated_columns)
        i += 1
        varslist += 1
       
    target_df.add_suffix(f'_yr{i}')
    merge_dfs.append(target_df)
    
    output = reduce(lambda left,right: pd.merge(left,right, left_index = True, right_index = True, how='inner'), merge_dfs)

    return output

#%%

testdf = harmonize_tracts(shp_merge_2020, input_dfs = [shp_merge_2010])



