###Calculating the Ding (2016) gentrification index###

import pandas as pd
import numpy as np


#%% 


def calc_ding( df_area, df_tract, cols_area = ['area_med_rent_yr1', 'area_med_rent_yr2', 'area_med_home_val_yr1', 'area_med_home_val_yr2', 'area_med_house_inc_yr1', 'area_med_house_inc_yr2'], cols_tract=['med_rent_yr1', 'med_rent_yr2', 'med_home_val_yr1', 'med_home_val_yr2', 'pop_25_over_yr1' 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1, ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2', 'ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2', 'ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2'], inplace = False):

    
    '''
    Parameters
   ----------
    df_area: dataframe  
        single row with columns for income variables at the county level
        
    df_tract: Geodataframe
        ACS variables at the tract level for a given time period
    
    cols_area: string list
        the column names for the fields used in the area calculations for the ding function and their corresponding ACS variable name
        0 'area_med_rent_yr1': B25064_001E
        1 'area_med_rent_yr2' : B25064_001E
        2 'area_med_home_val_yr1': B25077_001E
        3 'area_med_home_val_yr2' : B25077_001E
        4 'area_med_house_inc_yr1' : B19013_001E
        5 'area_med_house_inc_yr2' : B19013_001E
        
    cols_tract: string list
        the column names for the fields used at the tract level for the ding function and their corresponding ACS variable name
        0.'med_rent_yr1' : B25064_001E
        1 'med_rent_yr2': B25064_001E
        2 'med_home_val_yr1': B25077_001E
        3 'med_home_val_yr2': B25077_001E
        4 'pop_25_over_yr1' : B15002_001E
        5 'pop_25_over_yr2': B15002_001E
        6 'ba_degree_m_yr1': B15002_015E
        7 'ba_degree_m_yr2': B15002_015E
        8 'ma_degree_m_yr1':  B15002_016E
        9 'ma_degree_m_yr2':  B15002_016E
        10 'prof_degree_m_yr1': B15002_017E
        11 'prof_degree_m_yr2': B15002_017E
        12 'doc_degree_m_yr1': B15002_018E
        13 'doc_degree_m_yr2': B15002_018E
        14 'prof_degree_m_yr1': B15002_017E
        15 'prof_degree_m_yr2': B15002_017E
        16 'ba_degree_f_yr1': B15002_032E
        17 'ba_degree_f_yr2': B15002_032E
        18 'ma_degree_f_yr1':  B15002_033E
        19 'ma_degree_f_yr2':  B15002_033E
        20 'prof_degree_f_yr1': B15002_034E
        21 'prof_degree_f_yr2': B15002_034E
        23 'doc_degree_f_yr1': B15002_035E
        24 'doc_degree_f_yr2': B15002_035E
        25 'med_house_inc_yr1': B19013_001E
        26 'med_house_inc_yr2': B19013_001E
        
    inplace: Boolean
        If True returns input df with gent status and criteria columns appended,
        If False returns just GEOID, geometry, with gent status and criteria columns
       
    Returns
    --------
    GeoDataFrame
    
    
    Notes
    -------
    
    Resulting geodataframe will contain a 'gent_status' field that denotes the classification of each tract
    the possible options:
        0 'Weak Gentrification': tract gentrified during the time period and sits in the bottom quartile of gentrifying tracts based on home values and rents
        1'Moderate Gentrification': tract gentrified during the time period and sits in the middle two quartiles of gentrifying tracts based on home values or rents
        2'Intense Gentrification': tract gentrified during the time period and sits in the top quartile of gentrifying tracts based on home values or rents
        3'No Gentrification': the tract is able to gentrified but hasn't experienced gentrification during the time period
        4'Nongentrifiable': the tract is unable to gentrify
        
    References
    ----------------
    Ding, Lei "Gentrification and Resident Mobility in Philadelphia" Regional Science and Urban Economics, vol. 16, November 2016, pg 38-51 https://doi.org/10.1016/j.regsciureco.2016.09.004
    
       '''
       
# creating copies of input, used at the end for resulting DF dependent on inplace parameter choice

    copy_df = df_tract.copy(deep = True)
    df = df_tract.copy(deep=True)
    
# renaming columns for use in function, in case user wants to use their own
    
    rename_cols_tract = ['med_rent_yr1', 'med_rent_yr2', 'med_home_val_yr1', 'med_home_val_yr2', 'pop_25_over_yr1' 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1, ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2', 'ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2', 'ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2']
    cols_name_dict_tract = dict(zip(cols_tract, rename_cols_tract))
    
    df = df.rename( columns = cols_name_dict_tract)
    
    rename_cols_area = ['area_med_rent_yr1', 'area_med_rent_yr2', 'area_med_home_val_yr1', 'area_med_home_val_yr2', 'area_med_house_inc_yr1', 'area_med_house_inc_yr2']
    cols_name_dict_area = dict(zip(cols_area, rename_cols_area))
    df_area = df_area.rename(columns = cols_name_dict_area)
    
    #df = df.replace("-", np.nan)
    #df = df.replace(",", "", regex= True)
    #df = df.replace("2000+", "2000")
    
    
# Creating figures of total adult & adult educated population
    
    
    edu_male_yr1 = df['ba_degree_m_yr1'] + df['ma_degree_m_yr1'] + df['prof_degree_m_yr1'] + df['doc_degree_m_yr1']
    edu_male_yr2 = df['ba_degree_m_yr2'] + df['ma_degree_m_yr2'] + df ['prof_degree_m_yr2'] + df['doc_degree_m_yr2']
    
    edu_female_yr1 = df['ba_degree_f_yr1'] + df['ma_degree_f_yr1'] + df['prof_degree_f_yr1'] + df['doc_degree_f_yr1']
    edu_female_yr2 = df['ba_degree_f_yr2'] + df['ma_degree_f_yr2'] + df['prof_degree_f_yr2'] + df['doc_degree_f_yr2']
    
    
    
    df['edu_tot_pop_yr1'] = edu_male_yr1 + edu_female_yr1
    df['edu_tot_pop_yr2'] = edu_male_yr2 + edu_female_yr2
    
    
    
    
# Deriving change in share of college educated residents
    
    df['edu_perc_yr1'] = (df['edu_tot_pop_yr1'] / df['pop_25_over_yr1'])*100
    df['edu_perc_yr2'] = (df['edu_tot_pop_yr2'] / df['pop_25_over_yr2'])*100
    chg_edu_share = df['edu_perc_yr2'] - df['edu_perc_yr1']
    
# deriving changes in median rents and home values per tract
    
    chg_med_home_val = ((df['med_home_val_yr2'] - df['med_home_val_yr1']) / df['med_home_val_yr2'])*100
    chg_med_rent = ((df['med_rent_yr2'] - df['med_rent_yr1']) / df['med_rent_yr2'])*100
    
#  city wide figures
    
    area_pop_25_over_yr1 = df['pop_25_over_yr1'].sum()
    area_edu_tot_pop_yr1 = df['edu_tot_pop_yr1'].sum()
    area_edu_share_yr1 = (area_edu_tot_pop_yr1 / area_pop_25_over_yr1)*100
    
    area_pop_25_over_yr2 = df['pop_25_over_yr2'].sum()
    area_edu_tot_pop_yr2 = df['edu_tot_pop_yr2'].sum()
    area_edu_share_yr2 = (area_edu_tot_pop_yr2 / area_pop_25_over_yr2)*100
    
    area_chg_edu_share = area_edu_share_yr2 - area_edu_share_yr1
    
  
    area_home_val_perc_inc = ((df_area.iloc[0]['area_med_home_val_yr2'] - df_area.iloc[0]['area_med_home_val_yr1'])/ df_area.iloc[0]['area_med_home_val_yr2'])*100
    area_med_rent_perc_inc = ((df_area.iloc[0]['area_med_rent_yr2'] - df_area.iloc[0]['area_med_rent_yr1'])/ df_area.iloc[0]['area_med_rent_yr2'])*100
    
    #% Calculating ding index and creating a resulting dataframe with the tracts meeting the criteria
    
    df['gentrifiable'] = np.where(df['med_house_inc_yr1'] < df_area.iloc[0]['area_med_house_inc_yr1'], True, False)
    
    df['hhi_crit'] = np.where(df['gentrifiable'] == True, 1, 0)
    
    df['rent_crit'] = np.where(chg_med_rent > area_med_rent_perc_inc, .5, 0)
    
    df['val_crit'] = np.where(chg_med_home_val > area_home_val_perc_inc, .5, 0)
    
    df['edu_crit'] = np.where(chg_edu_share > area_chg_edu_share, 1, 0)
    
    
    df['crit'] = df['hhi_crit'] + df['rent_crit'] + df['val_crit'] + df['edu_crit']
    
    df['gentrifying'] = np.where(df['crit'] >= 2.5, True, False)
    
# creating a gent status column that gives more detail than a binary gentrifying y/n
    
    gent_only_df = df[df['gentrifying'] == True]
    
    quant_rent_vals = np.quantile(gent_only_df['med_rent_yr2'], [0, 0.25, 0.50, 0.75, 1])
    
    quant_home_vals = np.quantile(gent_only_df['med_home_val_yr2'], [0, 0.25, 0.50, 0.75, 1])
    
    conditions = [
        (df['gentrifying'] == True) & (df['med_rent_yr2'] <= quant_rent_vals[1]) & (df['med_home_val_yr2'] <= quant_home_vals[1]),
        (df['gentrifying'] == True) & ((df['med_rent_yr2'] <= quant_rent_vals[3]) | (df['med_home_val_yr2'] <= quant_home_vals[3])),
        (df['gentrifying'] == True) & ((df['med_rent_yr2'] > quant_rent_vals[3]) | (df['med_home_val_yr2'] > quant_home_vals[3])),
        (df['gentrifiable'] == True) & (df['gentrifying'] == False),
        (df['gentrifiable'] == False)
        ]
    
    choices = [
        'Weak Gentrification',
        'Moderate Gentrification',
        'Intense Gentrification',
        'No Gentrification',
        'Nongentrifiable'
        ]
    
    df['gent_status'] = np.select(conditions, choices)
    
    df = df[df['pop_25_over_yr1'] > 50]
    
    
    
    new_cols = df[['gentrifiable','gentrifying', 'hhi_crit', 'rent_crit', 'val_crit', 'edu_crit', 'crit', 'gent_status']].reset_index()
    
    keep_cols = df[[ 'GEOID', 'geometry']].reset_index()
    
    if inplace == False:
        output = pd.merge(keep_cols, new_cols, left_index = True, right_index = True)
    
    else:
        output = pd.merge(copy_df, new_cols, left_index = True, right_index = True)
    
    return output


