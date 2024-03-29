# PyGentrification: Gentrification Indices

A python package for calculating and visualizing gentrification indices from published academic research

## Description

The term “gentrification” encapsulates complex and interconnected social, economic, political, and physical processes that lead to a specific type of neighborhood change. Dr. Devin Bunten, an Assistant Professor of Urban Economics and Housing at MIT, defined gentrification as “…the territorial expansion of a wealthy community into a disinvested neighborhood, the installation of the social and legal regimes of the newcomers, and the deployment of new physical capital, both on a small scale – by homeowners undertaking renovations – and on a larger scale, by landed capitalists and public sector officials keen to raise revenue. It is the disruption and displacement of the original residents and their spatially realized social networks.” [^1] 
 

Government – at local, state, and federal lees – creates conditions that facilitate gentrification processes through targeted policy, investment, and subsidies. These conditions enable private actors, such as developers, lenders, builders, and real estate companies, to generate and accumulate wealth in neighborhoods that previously experienced chronic disinvestment[^2]. Together, these actors can “revitalize” a neighborhood, but with profit as their primary motivator, they have little incentive to consider the social and cultural fabric of a neighborhood or the communities that will be able to experience the benefits of their investment. 

Gentrification also requires newcomers. In early stages of gentrification, newcomers, who are often white with lower incomes and high levels of educational attainment, may be drawn to historically disinvested neighborhoods because of their need for affordable housing. These newcomers can serve as a signal of gentrification potential for developers and may advocate for new investment and amenities in their neighborhood. This neighborhood change, in turn, can draw wealthier newcomers who can afford increased housing costs[^2]. 

Gentrification is one cause of displacement. Residents in gentrifying neighborhoods can be forced to move due to increasing costs of rentals, property taxes, and local amenities, which can lead to evictions, foreclosures, and pressure for low-income homeowners to sell well below the market value of their homes to predatory buyers. Even if long-time residents do not physically move, they can experience displacement from their social networks, local culture, and sense of community[^2].   

Researchers have developed many methods to quantify, measure, and predict the complex processgentrification. These methods generally use on multiple indicators at several time periods. Researchers combine these indicators, as well as changes in those indicators over time, into an index that aim to quantify if the area has gentrified, if the area is vulnerable to gentrification, or some of other measure related to their particular theory of gentrification. Indicators often include measures related to race, educational attainment, housing costs, and housing tenure.

We developed this package to allow researchers to explore and compare different gentrification indices for their area of interest. The first version of this package has functions to calculate the indices from Bates (2013)[^3] and Ding et al. (2016)[^4], which both can be calculated from American Community Survey and Census data. 

### Bates (2013)

Bates (2013) calculated three indices using data from three years, each 10 years apart, (years 0-2) that together give a picture of gentrification in an area of interest: vulnerability to gentrification, presence of gentrification-related demographic change, and home value typology. The gentrification-related demographic change index is based on the gentrification index presented in Freeman (2005)[^5].   

#### Bates (2013) - Vulnerability to Gentrification
| Indicator      | Output values |  variable  |
| ------------------------------------ | ------------------------------------------ | -----------  |
| % Renters at census tract and county levels | 0: % Renters in tract < % Renters in county, 1: % Renters in tract > % Renters in county | renter_v  |
| % People of color at census tract and county levels | 0: % People of Color in tract < % People of Color in county, 1: % People of Color in tract > % People of Color in county | poc_v  |
| % People over 25 without a college degree at census tract and county levels | 0: % People over 25 without a college degree in tract < % People over 25 without a college degree in county, 1: % People over 25 without a college degree in tract > % People over 25 without a college degree in county  | nocollege_v  |
| Median Family Income at census tract and county levels | 0: Median Family Income in tract > Median Family Income in county, 1: Median Family Income in tract < Median Family Income in county | mfi_v  |
| **Vulnerability to Gentrification Index** | Score 0-4 (sum of 4 variables above)  |  v_index  |

#### Bates (2013) - Gentrification-Related Demographic Change
| Indicator      | Output values |  variable  |
| ------------------------------------ | ------------------------------------------ | -----------  |
| % Change in renters Year 1-2 at census tract and county levels | 0: % Change in renters in tract < % Renters in county, 1: % Change in renters in tract > % Change in renters in county | tenure_change  |
| % Change in People of color at census tract and county levels | 0: % Change in People of Color in tract < % Change in People of Color in county, 1: % Change in People of Color in tract > % Change in People of Color in county | race_change  |
| % Change in people over 25 without a college degree at census tract and county levels | 0: % Change in people over 25 without a college degree in tract < % Change in people over 25 without a college degree in county, 1: % Change in people over 25 without a college degree in tract > % Change in people over 25 without a college degree in county  | edu_change  |
| % Change in Median Household Income at census tract and county levels | 0: % Change in Median Household Income in tract > % Change in Median Household Income in county, 1: % Change Median Household Income in tract < % Change Median Household Income in county | income_change  |
| **Presence of Gentrification-Related Demographic Change Index**  | Score 0-4 (sum of 4 variables above)  |  dem_change_index  |

#### Bates (2013) - Home Value Typology
| Indicator      | Output values |  Variable  |
| ------------------------------------ | ------------------------------------------ | -----------  |
| Median home value in tract (year 0) | lowmod : bottom 3 quintiles, high: top 2 quintiles | homevalueq_yr0  |
| Median home value in tract (year 1) | lowmod : bottom 3 quintiles, high: top 2 quintiles | homevalueq_yr1  |
| Median home value in tract (year 2) | lowmod : bottom 3 quintiles, high: top 2 quintiles  | homevalueq_yr2  |
| Change in median home value year 0-1 | lowmod : bottom 3 quintiles, high: top 2 quintile | homevalueq_change_01  |
| Change in median home value year 1-2 | lowmod : bottom 3 quintiles, high: top 2 quintile | homevalueq_change_12  |
| Change in median home value year 0-2 | lowmod : bottom 3 quintiles, high: top 2 quintile | homevalueq_change_02  |
| **Home Value Typology Index**  | Each tract has a value of 'adjacent' (low or moderate Year 2 value, low or moderate Year 0 - Year 1 appreciation, touch boundary of one tract with high Year 2 value), 'accelerating' (low or moderate Year 2 value, high Year 1-Year 2 apprecation), 'appreciated' (low or moderate Year 0 value, high Year 2 value, high Year 0 -Year 2 appreciation), or 'no_typology'  |  mhv_type  |

#### Freeman (2005) Gentrification Index
| Indicator      | Output values |  Variable  |
| ------------------------------------ | ------------------------------------------ | -----------  |
| % housing units built in the last 20 years | 0: % new housing units in tract < % new housing in county , 1: % new housing units in tract < % new housing in count | newhouse_f_index  |
| % People over 25 without a college degree at census tract and county levels | 0: % People over 25 without a college degree in tract < % People over 25 without a college degree in county, 1: % People over 25 without a college degree in tract > % People over 25 without a college degree in county  | nocollege_f_index  |
| Median Household Income at census tract and county levels | 0: Median Household Income in tract > Median Household Income in county, 1: Median Household Income in tract < Median Household Income in county | mhi_f_index  |
| Median housing value at tract level years 1-2 | 0: median housing value in year 1 > median housing value in year 2, 1: median housing value in year 1 < median housing value in year 2 | mhv_f_index  |
| Freeman Gentrification Index  | Score 0-4 (sum of 4 variables above)  |  freeman  |

### Ding et al. (2016)

Ding et al. (2016) usese data from 2 years (years 1-2) to calculate one index that classifies tracts as experiencing intense gentrification, moderate gentrification, weak gentrification, no gentrification, or as non-gentrifiable.

#### Ding et a. (2016) - Gentrification Index
| Indicator      | Output values |  Variable  |
| ------------------------------------ | ------------------------------------------------ | -----------  |
| Median Household Income at census tract and county levels | 0 (gentrifiable = False): Median Household Income in tract > Median Household Income in county, 1 (gentrifiable = True): Median Household Income in tract < Median Household Income in county | hhi_crit, gentrifiable  |
| % Change in Median Rent at census tract and county levels | 0: % Change in Median Rent in tract < % Change in Median Rent in county, 0.5: % Change Median Rent in tract > % Change Median Rent in county | rent_crit  |
| % Change in Median Home Value at census tract and county levels | 0: % Change in Median Home Value in tract < % Change in Median Home Value in county, 0.5: % Change Median Home Value in tract > % Change Median Home Value in county | value_crit  |
| % Change in people over 25 without a college degree at census tract and county levels | 0: % Change in people over 25 without a college degree in tract < % Change in people over 25 without a college degree in county, 1: % Change in people over 25 without a college degree in tract > % Change in people over 25 without a college degree in county  | edu_crit  |
| Sum of Gentrification Criteria  |  0 - 3 (Sum of above 4 variables)  | crit  |
| Presence of Gentrification  |  False: crit < 2.5, True: crit>= 2.5  |  gentrifying  |
| **Gentrification Status**  | 'Weak Gentrification': meets gentrification criteria and in bottom two quartiles of criteria for change in median home values and rent, 'Moderate Gentrification': meets gentrification criteria and in middle two quartiles of criteria for change in median home values and rent, 'Strong Gentrification': meets gentrification criteria and in top quartile of criteria for change in median home values and rent, 'No Gentrification': tract is gentrifiable but does not meet gentrification criteria, 'Nongentrifiable': Does not meet income criteria in year 1 to be gentrifiable  |  gent_status  |

Both indices are calculated using data at the census tract level for a single county. This package include functions to directly the pull data from the American Community Survey and Census and their respective Tiger/Line geometries and combine data accross years with conflicting geometries using areal interpolation from the Tobler package. 

## Getting Started

### Dependencies

* Python 3.9.*
* numpy == 1.22.4
* pandas
* geopandas
* folium
* tobler
* branca
* requests


### Installing

```
pip install pygentrification
```
	
### Executing program

## API Calls

This module contains all the data requests a user might need to make to calculate the indices included in the package. This includes using 5 Year - American Community Survery, Dicennial Census, and TIGER Census data.

Each index requires data at the tract level and data for the county as a whole. Identiy the county and state using FIPS codes. 
The two example calls below would return the two dataframes needed to calculate the bates-freeman indices and ding index for Philadelphia County (101) in PA (42) using data from 2000, 2010, and 2020.

The function will return data in EPSG 4269, but requires a proj_parameter that indicates the projected crs that will be used for areal interpolation needed to harmonize data to census tract boundaries for different years.

```
from pygentrification.api_calls import get_api_data_tract, get_api_data_county

tract_gdf = get_api_data_tract("42", "101", years = [2000, 2010, 2020], indices = ["bates", "ding"], proj_crs = "EPSG: 2272")

county_gdf = get_api_data_county("42", "101", years = [2000, 2010, 2020], indices = ["bates", "ding"])

```


## Bates and Freeman Indices

This module contains the data prep steps, index calculation, and dataframe creation of the Bates-Freeman index


calc_batesfreeman is a function that calculates the index according to Bates-Freeman, as cited above. If using a GeoDataFrame retrieved with the functions above, an example call would be: 

```
from pygentrification.bates_freeman_indices import calc_bates_freeman

bates_freeman_gdf = calc_batesfreeman(county_gdf, tract_gdf, inplace = False)

```

Users may also use data retrieved in other ways as long as:
* one is a gdf at the tract level of the study area and one is a df or gdf values for the area as a whole 
* each dataset has data for the acs and census variables required for calculating the indices in this script for the years specified. 
* they specify column column names as a list with an order that corresponds exactly with the default values for th cols_tract and cols_area parameters.

```
cols_area = ['area_med_house_inc_yr1', 'area_med_house_inc_e_yr1', 'area_med_house_inc_yr2', 'area_med_house_inc_e_yr2', 'area_med_fam_inc_yr2', 'area_med_fam_inc_e_yr2']
cols_tract = ['pop_tenure_yr1', 'owner_yr1', 'renter_yr1', 'pop_tenure_yr2', 'owner_yr2', 'renter_yr2', 'pop_25_over_yr1', 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1', 'ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2','ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2','ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2','pop_race_yr1', 'white_yr1', 'pop_race_yr2', 'white_yr2', 'med_fam_inc_yr2', 'med_home_val_yr0', 'med_home_val_yr1', 'med_home_val_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2', 'tot_house_yr2', 'new_house_col1', 'new_house_col2', 'new_house_col3']
```
    

## Ding Index

This module contains the data prep steps, index calculation, and dataframe creation of the Ding index


calc_batesfreeman is a function that calculates the index according to Ding, as cited above. If using a GeoDataFrame retrieved with the functions above, an example call would be: 

```
from pygentrification.ding_index import calc_ding

ding_gdf = calc_ding(county_gdf, tract_gdf, inplace = False):

``` 

## Folium Maps

This module contains functions to create Folium maps from the output of Bates-Freeman and Ding functions hosted on a local HTML site.

The crs for the input gdf MUST be EPSG: 4269.

This function takes in the GeoDataFrame generated by the calc_batesfreeman function fand outputs and map object of a Folium map. It saves an html file of the map object to the working directory.

```
from pygentrification.folium_funcs import bates_freeman_result_map

bates_freeman_result_map(bates_freeman_gdf, filename = 'bates_freeman_map.html'):
```

This function takes in the GeoDataFrame generated by the calc_ding function fand outputs and map object of a Folium map. It saves an html file of the map object to the working directory.

```
from pygentrification.folium_funcs import ding_result_map 

ding_result_map(ding_gdf, filename = 'ding_map.html'):
```

Users may also use data retrieved in other ways as long as:
* one is a gdf at the tract level of the study area and one is a df or gdf values for the area as a whole 
* each dataset has data for the acs and census variables required for calculating the indices in this script for the years specified. 
* they specify column column names as a list with an order that corresponds exactly with the default values for th cols_tract and cols_area parameters.

```
cols_area = ['area_med_rent_yr1', 'area_med_rent_yr2', 'area_med_home_val_yr1', 'area_med_home_val_yr2', 'area_med_house_inc_yr1', 'area_med_house_inc_yr2']
cols_tract=['med_rent_yr1', 'med_rent_yr2', 'med_home_val_yr1', 'med_home_val_yr2', 'pop_25_over_yr1' 'ba_degree_m_yr1', 'ma_degree_m_yr1', 'prof_degree_m_yr1', 'doc_degree_m_yr1, ba_degree_f_yr1', 'ma_degree_f_yr1', 'prof_degree_f_yr1', 'doc_degree_f_yr1', 'pop_25_over_yr2', 'ba_degree_m_yr2', 'ma_degree_m_yr2', 'prof_degree_m_yr2', 'doc_degree_m_yr2', 'ba_degree_f_yr2', 'ma_degree_f_yr2', 'prof_degree_f_yr2', 'doc_degree_f_yr2', 'med_house_inc_yr1', 'med_house_inc_yr2']
```


## Authors

Contributors names and contact info

Winn Costantini (https://github.com/wcostantini)
Adam Thompson (https://github.com/Lubbles)
Josh Scrabeck (https://github.com/joshscrabeck)

## Version History

* 0.0.1
    *Initial release
* 0.0.2
* 0.0.3
* 0.0.4
* 0.0.5
    * Current Release

## License

This project is licensed under the BSD License - see the LICENSE.txt file for details

## Acknowledgments

Thanks to Lee Hachadoorian and the Temple University Geography and Urban Studies department. 

## References

[^1] Bunten, Devin M. “Untangling the Housing Shortage and Gentrification.” Bloomberg. October 23, 2019. [Link.](https://www.bloomberg.com/news/articles/2019-10-23/untangling-the-housing-shortage-and-gentrificatiom)
[^2] Zuk, Miriam, Ariel H. Bierbaum, Karen Chapple, Karolina Gorska, and Anastasia Loukaitou-Sideris. “Gentrification, Displacement, and the Role of Public Investment.” Journal of Planning Literature 33, no. 1 (February 1, 2018): 31–44. [https://doi.org/10.1177/0885412217716439.](https://doi.org/10.1177/0885412217716439)
[^3] Bates, Lisa. 2013. “Gentrification and Displacement Study: Implementing an Equitable Inclusive Development Strategy in the Context of Gentrification.” Urban Studies and Planning Faculty Publications and Presentations, May. [https://doi.org/10.15760/report-01.](https://doi.org/10.15760/report-01)
[^4] Freeman, Lance. 2005. “Displacement or Succession?: Residential Mobility in Gentrifying Neighborhoods.” Urban Affairs Review 40 (4): 463–91. [https://doi.org/10.1177/1078087404273341.](https://doi.org/10.1177/1078087404273341)
[^5] Ding, Lei, Jackelyn Hwang, and Eileen Divringi. 2016. “Gentrification and Residential Mobility in Philadelphia.” Regional Science and Urban Economics 61: 38–51. [https://doi.org/10.1016/j.regsciurbeco.2016.09.004.](https://doi.org/10.1016/j.regsciurbeco.2016.09.004)