
###Calculating the Bates (2013) gentrification indices and the Freeman (2005) gentrification index###

import pandas as pd
from math import sqrt
import numpy as np
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd

#%%

### MOE FUNCTIONS###

def moe_perc(den, num_e, den_e, prop):
    '''
    This function calculates the margin of error for a single derived proportion
    
    Parameters
    ----------------
    den: int or float
        denominator of proportion
    
    num_e: int or float
        calculated margin of error for numerator of proportion
        
    den_e: int or float
        calculated margin of error for denominator of proportion
        
    prop: float
        proportion 

    
    Returns
    ----------------
    float
    
    '''
    
    sqrt_a = (num_e**2)
    sqrt_b = ((prop**2) * (den_e)**2)
    sqrt_pos = sqrt_a - sqrt_b
    sqrt_neg = sqrt_a + sqrt_b

    moe = np.where(sqrt_a > sqrt_b, (1/den) * (np.sqrt(sqrt_pos)), (1/den) * (np.sqrt(sqrt_neg)) )
    
    return moe.item()


def moe_alltracts(df, col):
    ''' 
    This function calculates the margin of error for the summed value of a column (in this case, the aggregated value across all census tracts)
    
    Parameters
    ----------------
    df: df
    
   col: string
       name of column for which the margin of error is calculated

    
    Returns
    ----------------
    float
    
    '''
    
    x = df[col]**2
    
    moe = sqrt(x.sum())
    
    return moe

def moe_propagation(moe1, moe2):
    ''' 
    This function calculates the margin of error that results from propagation two margins of error
    
    Parameters
    ----------------
    moe1: int or float
        calculated margin of error 
    
    moe2: int or float
        calculated margin of error 
        
    Returns
    ----------------
    float
    '''

    moe = sqrt((moe1**2) + (moe2**2))
    
    return moe

#%%

def calc_batesfreeman(df_area, df_tract, cols_area = ['area_med_house_inc_yr1', 'area_med_house_inc_e_yr1', 'area_med_house_inc_yr2', 'area_med_house_inc_e_yr2', 'area_med_fam_inc_yr2', 'area_med_fam_inc_e_yr2'], cols_tract = ['pop_tenure_yr1', 'owner_yr1', 'renter_yr1', 'pop_tenure_yr2', 'owner_yr2', 'renter_yr2', 'pop_25_over_yr1', 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1', 'ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2','ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2','ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2','pop_race_yr1', 'white_yr1', 'pop_race_yr2', 'white_yr2', 'med_fam_inc_yr2', 'med_home_val_yr0', 'med_home_val_yr1', 'med_home_val_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2', 'tot_house_yr2', 'new_house_col1', 'new_house_col2', 'new_house_col3'], inplace = False):
    '''  
    
    Parameters
    ----------------
        
    df_area: df  
        single row with columns for income variables at the county-level
    
    df_tract: GeoDataFrame
         columns from American Community Survey (and Census if including data from 2000) for three different years that span 20 years in 10 year intervals (ex: year 0 = 2000, year 1 = 2010, and year 2 = 2020)
    
    cols_area: list of strings
        #Column names for ACS Variables - all adjusted for inflation#
        0 'area_med_house_inc_yr1': B19013_001E
        1 'area_med_house_inc_e_yr1': B19013_001M 
        2 'area_med_house_inc_yr2': B19013_001E
        3 'area_med_house_inc_e_yr2': B19013_001M
        4 'area_med_fam_inc_yr2': B19113_001E 
        5 'area_med_fam_inc_yr2': B19113_001M 
     
    cols_tract: list of strings
        #Column names for ACS and Census Variables - all monetary values adjusted for inflation#
        0 'pop_tenure_yr1': B25003_001E
        1 'owner_yr1': B25003_002E
        2 'renter_yr1': B25003_003E
        3 'pop_tenure_yr2': B25003_001E
        4 'owner_yr2': B25003_002E
        5 'renter_yr2': B25003_003E
        6 'pop_25_over_yr1': B15002_001E
        7 'ba_degree_m_yr1': B15002_015E
        8 'ma_degree_m_yr1':  B15002_016E
        9 'prof_degree_m_yr1': B15002_017E
        10 'doc_degree_m_yr1': B15002_018E
        11 'ba_degree_f_yr1': B15002_032E
        12 'ma_degree_f_yr1':  B15002_033E
        13 'prof_degree_f_yr1': B15002_034E
        14 'doc_degree_f_yr1': B15002_035E
        15 'pop_25_over_yr2': B15002_001E
        16 'ba_degree_m_yr2': B15002_015E
        17 'ma_degree_m_yr2':  B15002_016E
        18 'prof_degree_m_yr2': B15002_017E
        19 'doc_degree_m_yr2': B15002_018E
        20 'ba_degree_f_yr2': B15002_032E
        21 'ma_degree_f_yr2':  B15002_033E
        22 'prof_degree_f_yr2': B15002_034E
        23 'doc_degree_f_yr2': B15002_035E
        24 'pop_race_yr1': B03002_001E
        25 'white_yr1': B03002_003E
        26 'pop_race_yr2': B03002_001E
        27 'white_yr2': B03002_003E
        28 'med_fam_inc_yr2': B19113_001E
        29 'med_home_val_yr0': H085001, B25077_001E
        30 'med_home_val_yr1': B25077_001E
        31 'med_home_val_yr2': B25077_001E
        32 'med_house_inc_yr1': B19013_001E
        33 'med_house_inc_yr2': B19013_001E
        34 'tot_house_yr2': B25034_001E
        35 'new_house_col1': B25034_002E
        36 'new_house_col2': B25034_003E
        37 'new_house_col3': B25034_004E
        
    inplace: Boolean
        If TRUE, function returns the original/input df with new bates-freeman index columns appended, if FALSE returns just GEOID, geometry, and the newly generated indices columns
    
    Returns
    ----------------
    GeoDataFrame
    
    
    Notes
    ----------------
    The GeoDataFrame will contain columns with values related to four indices:
    
    #Bates Vulnerability Index#
    'renter_v': If % renters of a tract is > % renters city wide (minus margin of error) then value is 1, if not then value is 0
    'poc_v': If % people of color (calculated as total population - white non-hispanic population) of a tract is > % people of color city wide (minus margin of error) then value is 1, if not then value is 0
    'nocollege_v' ;If % people without a college degree (highest level of educational attainment is less than an associate's degree) of a tract is > % population with a colege degree city wide (minus margin of error) then value is 1, if not then value is 0
    'mfi_v' ; If median family income of a tract is < 80% of median family income city wide (plus margin of error) then value is 1, if not then value is 0
    'v_index': The sum of the the above vulnerability variables to get a integer value of 0-4. Tracts that are vulnerable to gentrification are considered 'gentrifiable'
    
    #Bates Gentrification-Related Demographic Change Index#
    'tenure_change': If  percentage point change in the % of owners in a tract is > the change city wide (minus margin of error) over 10 years then value is 1, if not then value is 0
    'race_change': If  percentage point change in the % white non-hispanic people in a tract is > the change city wide (minus margin of error) over 10 years then value is 1, if not then value is 0
    'edu_change': If  percentage point change in the % of people with a college degree or higher in a tract is > the change city wide (minus margin of error) over 10 years then value is 1, if not then value is 0
    'income_change': If percent change in the median household income in a tract is > the change city wide (minus margin of error) over 10 years then value is 1, if not then value is 0
    'dem_change_index': TRUE if threshold is met for 3 out of four categories OR if meets threshold for %white and % 25+ with college degree, if not then value is FALSE
    
    #Bates Home Value Typologies Index#
    'homevalueq_yr0': The median home values of each tract in year 0 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'homevalueq_yr1': The median home values of each tract in year 1 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'homevalueq_yr2': The median home values of each tract in year 2 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'homevalueq_change_01': The change in median home values of each tract from year 0 to year 1 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'homevalueq_change_12': The change in median home values of each tract from year 1 to year 2 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'homevalueq_change_02': The change in median home values of each tract from year 0 to year 2 were separated into quantiles. The top two quantiles have the value "high" and the bottom three have the value "lowmed"
    'mhv_type':  Each tract has a value of 'adjacent' (low or moderate Year 2 value, low or moderate YEar 0-Year 1 appreciation, touch boundary of one tract with high Year 2 value), 'accelerating' (low or moderate Year 2 value, high Year 1-Year 2 apprecation), 'appreciated' (low or moderate Year 0 value, high Year 2 value, high Year 0-Year 2 appreciation), or 'no_typology'
    
    #Freeman Index# ***This function assumes that all tracts analyzed meet Freeman's critera of being in the "central city" of a metropolitan area***
    'newhouse_f_index': If the % housing build in last 20 years in each tract in in year 2 is below the area median then value is 1, if not then value is 0
    'nocollege_f_index': If change in % 25+ without a college degree year 1 to year 2 is above the area percentage point change then value is 1, if not then value is 0
    'mhi_f_index': If median household income in year 1 for each tract is < the city wide mhi in year 1 then value is 1, if not then value is 0
    'mhv_f_index': If median housing value increased in a tract from year 1 to year 2 then value is 1, if not then value is 0
    'freeman': The sum of the the above variables to get a integer value of 0-4

    
    References
    ----------------
    Bates, Lisa. 2013. “Gentrification and Displacement Study: Implementing an Equitable Inclusive Development Strategy in the Context of Gentrification.” Urban Studies and Planning Faculty Publications and Presentations, May. https://doi.org/10.15760/report-01.

    Freeman, Lance. 2005. “Displacement or Succession?: Residential Mobility in Gentrifying Neighborhoods.” Urban Affairs Review 40 (4): 463–91. https://doi.org/10.1177/1078087404273341. *
    *This function assumes that all tracts in the analysis meet Freeman's definition of being in the "central city"
    
    '''
   
    ###prep data###
   
    df_tract = gpd.GeoDataFrame(df_tract, crs = 'EPSG:4269', geometry = 'geometry')
   
    
    ##create two deep copies##
    
    #the first will be used at the end of the function to return the orginal input df with the new output columns appended
    #the second will make a copy that the rest of the function uses to calculate all intermediate columns (needed to caclulate final output columns) without adding them to the initial input df
    copy_df = df_tract.copy(deep = True)
    df = df_tract.copy(deep = True)    
    
    #rename columns for use in function
    cols_tract_rename = ['pop_tenure_yr1', 'owner_yr1', 'renter_yr1', 'pop_tenure_yr2', 'owner_yr2', 'renter_yr2', 'pop_25_over_yr1', 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1', 'ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2','ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2','ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2','pop_race_yr1', 'white_yr1', 'pop_race_yr2', 'white_yr2', 'med_fam_inc_yr2', 'med_home_val_yr0', 'med_home_val_yr1', 'med_home_val_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2', 'tot_house_yr2', 'new_house_col1', 'new_house_col2', 'new_house_col3']
    col_name_dict_tract = dict(zip(cols_tract, cols_tract_rename))
    
    df = df.rename(columns = col_name_dict_tract)

    
    df = df.loc[(df['pop_race_yr2'].astype(int) >= 50) & (df['tot_house_yr2'].astype(int) > 0)]
    
    cols_area_rename = ['area_med_house_inc_yr1', 'area_med_house_inc_e_yr1', 'area_med_house_inc_yr2', 'area_med_house_inc_e_yr2', 'area_med_fam_inc_yr2', 'area_med_fam_inc_e_yr2']
    col_name_dict_area = dict(zip(cols_area, cols_area_rename))
    
    df_area = df_area.rename(columns = col_name_dict_area)
    
    
    ###CREATE DERIVED COLUMNS AND VALUES NEEDED FOR INDICES###

    ##TENURE##

    #create new columns with proportion of renters in each tract for years 1 and 2
    df['renterp_yr1'] = df['renter_yr1']/df['pop_tenure_yr1']
    df['ownerp_yr1'] = 1 - df['renterp_yr1']
    df['renterp_yr2'] = df['renter_yr2']/df['pop_tenure_yr2']
    df['ownerp_yr2'] = 1 - df['renterp_yr2']

    #calculate the area proportion of renters for years 1 and 2
    area_renters_1 = df['renter_yr1'].sum()
    area_tenure_1 = df['pop_tenure_yr1'].sum()

    area_renters_2 = df['renter_yr2'].sum()
    area_tenure_2 = df['pop_tenure_yr2'].sum()

    area_renter_p_1 = area_renters_1/area_tenure_1
    area_owner_p_1 = 1 - area_renter_p_1
    area_renter_p_2 = area_renters_2/area_tenure_2
    area_owner_p_2 = 1 - area_renter_p_2

    #calculate the area moe for the number of renters and total number of households for years 1 and 2
    area_owner_e_1 = moe_alltracts(df, 'owner_yr1')
    area_tenure_e_1 = moe_alltracts(df, 'pop_tenure_yr1' )

    area_renter_e_2 = moe_alltracts(df, 'renter_yr2')
    area_owner_e_2 = moe_alltracts(df, 'owner_yr2')
    area_tenure_e_2 = moe_alltracts(df, 'pop_tenure_yr2')

    #assign variables to calculate moe for area proportion of owners for year 1
    den_1 = area_tenure_1
    num_e_1 = area_owner_e_1
    den_e_1 = area_tenure_e_1
    prop_1 = area_owner_p_1

    #use moe_perc function for year 1
    area_owner_moe_1 = moe_perc(den_1, num_e_1, den_e_1, prop_1)

    #assign variables to calculate moe for area proportion of owners and renters for year 2
    den_2 = area_tenure_2
    num_e_2 = area_owner_e_2
    den_e_2 = area_tenure_e_2
    prop_2 = area_owner_p_2

    #use moe_perc function for year 2 powners
    area_owner_moe_2 = moe_perc(den_2, num_e_2, den_e_2, prop_2)

    den_3 = area_tenure_2
    num_e_3 = area_renter_e_2
    den_e_3 = area_tenure_e_2
    prop_3 = area_renter_p_2

    #use moe_perc function for year 2 renters
    area_renter_moe_2 = moe_perc(den_3, num_e_3, den_e_3, prop_3)

    #For each tract, calculate change percentage point change of owners from year 1 to year 2
    df['owner_change'] = df['ownerp_yr2'] - df['ownerp_yr1']

    #calculate the area percentage point change from year 1 to year 2 and the moe
    area_owner_change = area_owner_p_2 - area_owner_p_1

    area_owner_change_e = moe_propagation(area_owner_moe_1, area_owner_moe_2)


    ##RACE AND ETHNICITY##

    #calculate proportion of POC and white pop for each tract for years 1 and 2
    df['poc_yr1'] = df['pop_race_yr1'] - df['white_yr1']
    df['pocp_yr1'] = (df['poc_yr1']/df['pop_race_yr1'])
    df['whitep_yr1'] = 1 - df['pocp_yr1']

    df['poc_yr2'] = df['pop_race_yr2'] - df['white_yr2']
    df['pocp_yr2'] = (df['poc_yr2']/df['pop_race_yr1'])
    df['whitep_yr2'] = 1 - df['pocp_yr2']

    #Calculate area proportion of people of color for years 1 and 2
    area_pop_race_1 = df['pop_race_yr1'].sum()
    area_poc_1 = df['poc_yr1'].sum()
    area_poc_p_1 = area_poc_1/area_pop_race_1
    area_white_p_1 = 1 - area_poc_p_1 

    area_pop_race_2 = df['pop_race_yr2'].sum()
    area_poc_2 = df['poc_yr2'].sum()
    area_poc_p_2 = area_poc_2/area_pop_race_2
    area_white_p_2 = 1 - area_poc_p_2 

    #calculate the area moe for the number of poc and total pop for years 1 and 2
    area_white_e_1 = moe_alltracts(df, 'white_yr1')
    area_pop_race_e_1 = moe_alltracts(df, 'pop_race_yr1')

    area_poc_e_2 = moe_alltracts(df, 'poc_yr2')
    area_white_e_2 = moe_alltracts(df, 'white_yr2')
    area_pop_race_e_2 = moe_alltracts(df, 'pop_race_yr2')

    #assign variables to calculate moe for area proportion for year 1 for white pop
    den_4 = area_pop_race_1
    num_e_4 = area_white_e_1
    den_e_4 = area_pop_race_e_1
    prop_4 = area_white_p_1

    #use moe_perc function for year 1
    area_white_moe_1 = moe_perc(den_4, num_e_4, den_e_4, prop_4)

    #assign variables to calculate moe for area proportion for year 2 for poc and white pop
    den_5 = area_pop_race_2
    num_e_5 = area_poc_e_2
    den_e_5 = area_pop_race_e_2
    prop_5 = area_poc_p_2

    #use moe_perc function for year 2 - poc
    area_poc_moe_2 = moe_perc(den_5, num_e_5, den_e_5, prop_5)

    den_6 = area_pop_race_2
    num_e_6 = area_white_e_2
    den_e_6 = area_pop_race_e_2
    prop_6 = area_white_p_2

    #use moe_perc function for year 2 - white
    area_white_moe_2 = moe_perc(den_6, num_e_6, den_e_6, prop_6)

    #for each tract, calculate change percentage point change from year 1 to year 2
    df['white_change'] = df['whitep_yr2'] - df['whitep_yr1']

    #calculate the area percentage point change from year 1 to year 2 and the moe
    area_white_change = area_white_p_2 - area_white_p_1
    area_white_change_e = moe_propagation(area_white_moe_1, area_white_moe_2)

    ##EDUCATIONAL ATTAINMENT##

    #calculate proportion 25+ population with and without a college degree for each tract for years 1 and 2
    df['pop_25_over_edu_yr1'] =  df['ba_degree_m_yr1'] + df['ma_degree_m_yr1'] + df['prof_degree_m_yr1'] + df['doc_degree_m_yr1'] + df['ba_degree_f_yr1'] + df['ma_degree_f_yr1'] + df['prof_degree_f_yr1'] + df['doc_degree_f_yr1']
    df['nocollege_yr1'] = df['pop_25_over_yr1'] - df['pop_25_over_edu_yr1']
    df['college_yr1'] = df['pop_25_over_edu_yr1']

    df['nocollegep_yr1'] = df['nocollege_yr1'] / df['pop_25_over_yr1']
    df['collegep_yr1'] = 1 - df['nocollegep_yr1']
    
    df['pop_25_over_edu_yr2'] =  df['ba_degree_m_yr2'] + df['ma_degree_m_yr2'] + df['prof_degree_m_yr2'] + df['doc_degree_m_yr2'] + df['ba_degree_f_yr2'] + df['ma_degree_f_yr2'] + df['prof_degree_f_yr2'] + df['doc_degree_f_yr2']

    df['nocollege_yr2'] = df['pop_25_over_yr2'] - df['pop_25_over_edu_yr2']
    df['college_yr2'] = df['pop_25_over_edu_yr2']

    df['nocollegep_yr2'] = df['nocollege_yr2'] / df['pop_25_over_yr2']
    df['collegep_yr2'] = 1 - df['nocollegep_yr2']

    #calculate area proportion of people without a college degree for years 1 and 2
    area_pop_edu_1 =  df['pop_25_over_yr1'].sum()
    area_nocollege_1 = df['nocollege_yr1'].sum()
    area_nocollege_p_1 = area_nocollege_1/area_pop_edu_1
    area_college_p_1 = 1 - area_nocollege_p_1

    area_pop_edu_2 = df['pop_25_over_yr2'].sum()
    area_nocollege_2 = df['nocollege_yr2'].sum()
    area_nocollege_p_2 = area_nocollege_2/area_pop_edu_2
    area_college_p_2 = 1 - area_nocollege_p_2


    #calculate the area moe for the number of people w/o college degrees and total pop for years 1 and 2
    area_college_e_1 = moe_alltracts(df, 'college_yr1')
    area_pop_edu_e_1 = moe_alltracts(df,  'pop_25_over_yr1' )

    area_nocollege_e_2 = moe_alltracts(df, 'nocollege_yr2')
    area_college_e_2 = moe_alltracts(df, 'college_yr2')
    area_pop_edu_e_2 = moe_alltracts(df, 'pop_25_over_yr2')

    #assign variables to calculate moe for area proportion for year 1 - college
    den_7 = area_pop_edu_1
    num_e_7 = area_college_e_1
    den_e_7 = area_pop_edu_e_1
    prop_7 = area_college_p_1

    #use moe_perc function for year 1
    area_college_moe_1 = moe_perc(den_7, num_e_7, den_e_7, prop_7)

    #assign variables to calculate moe for area proportion for year 2 - college and no college
    den_8 = area_pop_edu_2
    num_e_8 = area_nocollege_e_2
    den_e_8 = area_pop_edu_e_2
    prop_8 = area_nocollege_p_2

    #use moe_perc function for year 2 - no college
    area_nocollege_moe_2 = moe_perc(den_8, num_e_8, den_e_8, prop_8)

    den_9 = area_pop_edu_2
    num_e_9 = area_college_e_2
    den_e_9 = area_pop_edu_e_2
    prop_9 = area_college_p_2

    #use moe_perc function for year 2 - college
    area_college_moe_2 = moe_perc(den_9, num_e_9, den_e_9, prop_9)

    #For each tract, calculate change percentage point change from year 1 to year 2
    df['college_change'] = df['collegep_yr2'] - df['collegep_yr1']

    #Calculate the area percentage point change from year 1 to year 2 and the moe
    area_college_change = area_college_p_2 - area_college_p_1

    area_college_change_e = moe_propagation(area_college_moe_1, area_college_moe_2)


    ##MEDIAN HOUSEHOLD INCOME##

    #assign variables for area mhi years 1 and 2 adding moe
    area_mhi_1 = df_area.iloc[0]['area_med_house_inc_yr1'] + df_area.iloc[0]['area_med_house_inc_e_yr1']
    area_mhi_2 = df_area.iloc[0]['area_med_house_inc_yr2'] + df_area.iloc[0]['area_med_house_inc_e_yr2']

    #for each tract, calculate change in mhi from year 1 to year 2
    df['mhip_change'] = (df['med_house_inc_yr2'] - df['med_house_inc_yr1'])/df['med_house_inc_yr2']

    #calculate the area change in mhi from year 1 to year 2 and the moe
    area_mhi_pchange = (area_mhi_2 - area_mhi_1)/area_mhi_2

    ##MEDIAN FAMILY INCOME##
    
    #add the moe to the area median family income for year 2 and find 80% of that value 
    area_mfi_2 = df_area.iloc[0]['area_med_fam_inc_yr2'] + df_area.iloc[0]['area_med_fam_inc_e_yr2']
    area_mfi_threshold = area_mfi_2 * 0.8 #threshold is 80% of median mfi

    
    ###INDEX 1: BATES (2013) VULNERABILITY SCORE###

    #this index will use ACS values from year 2#

    ##TENURE##

    #calculate threshold for proportion of renters
    area_renter_threshold = area_renter_p_2 - area_renter_moe_2

    #calculate whether the % renters each tract is at or above the area median (minus the moe)
    df['renter_v'] = np.where(df['renterp_yr2'] >= area_renter_threshold, 1, 0)

    ##RACE AND ETHNICITY##

    #calculate threshold for proportion of poc
    area_poc_threshold = area_poc_p_2 - area_poc_moe_2

    #calculate whether the % POC of each tract is at above the area median (minus moe)
    df['poc_v'] = np.where(df['pocp_yr2'] >= area_poc_threshold, 1, 0)


    ##EDUCATIONAL ATTAINMENT##

    #calculate threshold for proportion of people 25+ without college degrees
    area_nocollege_threshold = area_nocollege_p_2 - area_nocollege_moe_2

    #calculate whether the % 25+ without college deg for each tract is at above the area median (minus moe)
    df['nocollege_v'] = np.where(df['nocollegep_yr2'] >= area_nocollege_threshold, 1, 0)


    ##MEDIAN FAMILY INCOME##
    
    #caluclate whether the MFI for each tract is at or below 80% of the area MFI (plus moe)
    df['mfi_v'] = np.where(df['med_fam_inc_yr2'] <= area_mfi_threshold, 1, 0)


    ##TOTAL VULNERABILITY  SCORE##
    
    #calculate score 0-4, weight of 1 for each category and create new column (and/or pandas series)
    df['v_index'] = df['renter_v'] + df['poc_v'] + df['nocollege_v'] + df['mfi_v']


    ###INDEX 2: GENTRIFICATION RELATED DEMOGRAPHIC CHANGE###


    ##TENURE##
    
    #for each tract, calculate if proportion of owners Year 1-Year 2 increased or decreased less the   area percentage point change (minus MOE)
    area_ownerchange_threshold = area_owner_change - area_owner_change_e
    df['tenure_change'] = np.where(df['owner_change'] > area_ownerchange_threshold, 1, 0) 


    ##RACE AND ETHNICITY##
    
    #for each tract, calculate if proportion of white pop Year 1-Year 2 increased or decreased less the area percentage point change (minus MOE)
    area_whitechange_threshold = area_white_change - area_white_change_e
    df['race_change'] = np.where(df['white_change'] > area_whitechange_threshold, 1, 0) 


    ##EDUCATIONAL ATTAINMENT##
    
    #for each tract, calculate if change in proportion of 25+ without a college degree Year 1-Year 2 is above or below the area percentage point change (add or subtact MOE)
    area_collegechange_threshold = area_college_change - area_college_change_e
    df['edu_change'] = np.where(df['college_change'] > area_collegechange_threshold, 1, 0) 


    ##MHI##
    
    #for each tract, calculate if percent change in MHI Year 1-Year 2 is above or below the area percent change (add or subtact MOE)
    df['income_change'] = np.where(df['mhip_change'] > area_mhi_pchange, 1, 0) 

    ##SCORE: GENTRIFICATION RELATED DEMOGRAPHIC CHANGE (TRUE OR FALSE)##
    
    #YES if threshold is met for 3 out of four categories OR if meets threshold for %white and % 25+ with college degree          
    df['dem_change_index'] = np.where((df['tenure_change'] + df['race_change'] +  df['edu_change'] + df['income_change']) >=3, True, np.where((df['race_change'] + df['edu_change']) == 2, True, False ))
    
    ###INDEX 3: HOUSING MARKET CONDITIONS###

    ##2000, Year 1, AND Year 2 VALUES##
    
    #calculate quintiles for year 0 and year 2

    #year 0
    df['homevalueq_yr0'] = pd.qcut(df['med_home_val_yr0'], 5, labels = [0,1,2,3,4]).astype('int')
    df['homevalueq_yr0'] = np.where(df['homevalueq_yr0'] <= 2, 'lowmod', 'high')

    #year 2
    df['homevalueq_yr2'] = pd.qcut(df['med_home_val_yr2'], 5, labels = [0,1,2,3,4]).astype('int')
    df['homevalueq_yr2'] = df['homevalueq_yr2'] = np.where(df['homevalueq_yr2'] <= 2, 'lowmod', 'high')

    ##CHANGE YEAR 0 - YEAR 1##
    
    #calculate change in median value for each tract and quintiles
    df['homevalueq_change_01'] = df['med_home_val_yr1'] - df['med_home_val_yr0']
    df['homevalueq_change_01'] = pd.qcut(df['homevalueq_change_01'], 5, labels = [0,1,2,3,4]).astype('int')
    df['homevalueq_change_01'] = np.where(df['homevalueq_change_01'] <= 2, 'lowmod', 'high')


    ##CHANGE YEAR 1- YEAR 2##
    
    #calculate change in median value for each tract and quintiles
    df['homevalueq_change_12'] = df['med_home_val_yr2'] - df['med_home_val_yr1']
    df['homevalueq_change_12'] = pd.qcut(df['homevalueq_change_12'], 5, labels = [0,1,2,3,4]).astype('int')
    df['homevalueq_change_12'] = np.where(df['homevalueq_change_12'] <= 2, 'lowmod', 'high')

    ##CHANGE YEAR 0 - YEAR 2##
    
    #calculate change in median value for each tract and quintiles
    df['homevalueq_change_02'] = df['med_home_val_yr2'] - df['med_home_val_yr0']
    df['homevalueq_change_02'] = pd.qcut(df['homevalueq_change_02'], 5, labels = [0,1,2,3,4]).astype('int')
    df['homevalueq_change_02'] = np.where(df['homevalueq_change_02'] <= 2, 'lowmod', 'high')

    ##TYPLOGY##

    #create bool column to check if each tract has high Year 2 value and/or touches a tract with a high Year 2 value
    df['adjacent_list'] = None  
    df['adjacent_high_yr2'] = None

    for index, row in df.iterrows():   

        # get 'not disjoint' tracts
        neighbors = df[~df.geometry.disjoint(row.geometry)].homevalueq_yr2.tolist()

        # add names of neighbors as NEIGHBORS value
        df.at[index, 'adjacent_list'] = neighbors

        if (neighbors.count('high') == 1) & (row.homevalueq_yr2 == 'high'):
            df.at[index, 'adjacent_high_yr2'] = False
    
        elif ('high' in neighbors):
            df.at[index, 'adjacent_high_yr2'] = True
        
        else:
            df.at[index, 'adjacent_high_yr2'] = False
        
        #Create row for housing value typology

    #adjacent: low or moderate Year 2 value, low or moderate 2000-Year 1 appreciation, touch boundary of one tract with high Year 2 value
    #accelerating: low or moderate Year 2 value, high Year 1-Year 2 apprecation
    #appreciated: low or moderate 2000 value, high Year 2 value, high 2000-Year 2 appreciation

    df['mhv_type'] = None
    for index, row in df.iterrows():
    
        if (row.homevalueq_yr2 == 'lowmod') & (row.homevalueq_change_01 == 'lowmod') & (row.adjacent_high_yr2 == True):
        
            df.at[index, 'mhv_type'] = 'adjacent'
        
        elif (row.homevalueq_yr2 == 'lowmod') & (row.homevalueq_change_12 == 'high'):
        
            df.at[index, 'mhv_type'] = 'accelerating'
        
        elif (row.homevalueq_yr0 == 'lowmod') & (row.homevalueq_yr2 == 'high') & (row.homevalueq_change_02 == 'high'):
        
            df.at[index, 'mhv_type'] = 'appreciated'
        
        else:
        
            df.at[index, 'mhv_type'] = 'no_typology'


    ###INDEX 4: FREEMAN INDEX###

    ##YEAR STRUCTURE BUILT##
    
    #calculate whether the % housing build in last 20 years in each tract in year 2 is below the area median (yes or no)
    if len(cols_tract) == 37: #calculating the # of housing built in the last 20 years will require 2 or 3 columns from the ACS
        
        df['newhousp'] = (df['new_house_col1_yr2'].astype(int) + df['new_house_col2_yr2'].astype(int)) / df['tot_house_yr2'].astype(int)
    
    else: 
        
        df['newhousp'] = (df['new_house_col1_yr2'].astype(int) + df['new_house_col2_yr2'].astype(int) + df['new_house_col3_yr2'].astype(int))/df['tot_house_yr2'].astype(int)
    
    area_newhous_med = df['newhousp'].median()  
    df['newhous_f_index'] = np.where(df['newhousp'] < area_newhous_med, 1, 0)


    ##EDUCATIONAL ATTAINMENT##
    #for each tract, calculate change in % 25+ without a college degree year 1 to year 2 and if this change is above the area percentage point change (without subtracting the MOE) (yes or no)
    df['nocollege_change'] = df['nocollegep_yr2'] - df['nocollegep_yr1']
    area_nocolch = (df['nocollege_yr2'].sum()/df['pop_25_over_yr2'].sum()) - (df['nocollege_yr1'].sum()/df['pop_25_over_yr1'].sum())
    df['nocollege_f_index'] = np.where(df['nocollege_change'] > area_nocolch, 1, 0)


    ##MEDIAN HOUSEHOLD INCOME##
    #calcuate if median household income in year 1 is < the area mhi (yes or no)
    df['mhi_f_index'] = np.where(df['med_house_inc_yr1'] < df_area.iloc[0]['area_med_house_inc_yr1'], 1, 0 )
    
    ##HOUSING VALUE##
    #calcuate if median housing values year 1 to year 2 increased (yes or no)
    df['mhv_f_index'] = np.where((df['med_home_val_yr2'] - df['med_home_val_yr1']) > 0, 1, 0)

    ##FREEMAN SCORE##
    #to be considered gentrifying, tract must meet fufill all categories 
    df['freeman'] = np.where((df['newhous_f_index'] + df['nocollege_f_index'] + df['mhi_f_index'] +    df['mhv_f_index']) == 4, True, False)
    
    
    ###CREATE OUTPUT DATAFRAMES###
    newcolumns = df[['renter_v', 'poc_v', 'nocollege_v', 'mfi_v', 'v_index', 'tenure_change', 'race_change', 'edu_change', 'income_change', 'dem_change_index','homevalueq_yr0', 'homevalueq_yr2','homevalueq_change_01','homevalueq_change_12','homevalueq_change_02','mhv_type', 'newhous_f_index', 'nocollege_f_index','mhi_f_index','mhv_f_index','freeman']].reset_index(drop =  True)
    keepcolumns =df[[ 'GEOID','geometry']].reset_index(drop = True)
    
    if inplace == False:
        output = pd.merge(keepcolumns, newcolumns, left_index= True, right_index = True)
    
    else:
        output = pd.merge(copy_df, newcolumns, left_index= True, right_index = True)
        
        
    return output



