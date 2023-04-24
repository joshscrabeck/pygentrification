#The harmonization function used in the api_calls module to combine acs and census data with different geometries#

from tobler.area_weighted import area_interpolate
from functools import reduce
import geopandas as gpd

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



