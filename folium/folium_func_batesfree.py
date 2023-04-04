# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 00:47:32 2023

@author: tul54884
"""

import pandas as pd
import os
import numpy as np
import geopandas as gpd
import folium as f

#%%

def bates_freeman_result_map(result_df = output):
    
    def dem_change_index_color(feature):
        if feature ['properties']['dem_change_index']== True :
            return 'orange'
        else:
            return 'white'
    
    def vuln_index_color(feature):
        if feature ['properties']['v_index'] == 0:
            return '#fee5d9'
        if feature ['properties']['v_index'] == 1:
            return '#fcae91'
        if feature ['properties']['v_index'] == 2:
            return '#fb6a4a'
        if feature ['properties']['v_index']== 3:
            return '#de2d26'
        if feature ['properties']['v_index']== 4:
            return '#a50f15'
        
    
    def housing_typology_index_color(feature):
        if feature['properties']['mhv_type']== 'no typology':
            return 'white'
        if feature['properties']['mhv_type']== 'adjacent':
            return '#fde0dd'
        if feature['properties']['mhv_type']== 'accelerating':
            return '#fa9fb5'
        if feature['properties']['mhv_type']== 'appreciated':
            return '#c51b8a'
        
    def freeman_index_color(feature):
        if feature['properties']['freeman']== 0:
            return 'white'
        if feature['properties']['freeman']== 1:
            return '#bdd7e7'
        if feature['properties']['freeman']== 2:
            return '#6baed6'
        if feature['properties']['freeman']== 3:
            return '#3182bd'
        if feature['properties']['freeman']== 4:
            return '#08519c'

    
    
    
    m = f.Map(
        location= [
            sum(result_df.geometry.total_bounds[[1, 3]]) / 2,
            sum(result_df.geometry.total_bounds[[0, 2]]) / 2 
        ],
        tiles= '',
        zoom_start= 11
        )
    
    base_map = f.FeatureGroup(name='basemap',
                              overlay = False,
                              control = False)
    f.TileLayer(tiles = 'cartodbpositron').add_to(base_map)
    base_map.add_to(m)
    
    
    dem_chg_layer_fg = f.FeatureGroup(name='Demographic Change Index', show = False)
    
    dem_chg_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip = f.GeoJsonTooltip(fields=['dem_change_index']),   #perhaps Winn wants a different popup value?
        style_function = lambda feature: {'fillColor': dem_change_index_color(feature),
                                          'fillOpacity':0.5,
                                          'weight':0},
        name= 'Demographic Change Index'
        ))
    
    
    vuln_ind_layer_fg = f.FeatureGroup(name= 'Vulnerability Index', show= False)
    
    vuln_ind_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip= f.GeoJsonTooltip(fields= ['v_index']),
        style_function = lambda feature:{'fillColor': vuln_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight': 0},
        name = 'Vulnerability Index'
             ))
    
    
    
    house_typo_layer_fg = f.FeatureGroup(name = 'Housing Typology Index', show=False)
    
    house_typo_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip= f.GeoJsonTooltip(fields= ['mhv_type']),
        style_function= lambda feature: {'fillColor': housing_typology_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight':0},
        name = 'Housing Typology Index'
            ))
    
    
    
    freeman_layer_fg = f.FeatureGroup(name= 'Freeman Index', show=False)
    
    freeman_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip=f.GeoJsonTooltip(fields= ['freeman']),
        style_function= lambda feature: {'fillColor': freeman_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight':0},
        name= 'Freeman Index'
        ))
    
    freeman_layer_fg.add_to(m)
    house_typo_layer_fg.add_to(m)
    vuln_ind_layer_fg.add_to(m)
    dem_chg_layer_fg.add_to(m)
    f.LayerControl().add_to(m)
    
    return m
    
    #%%
    
    
    bates_freeman_result_map().save('testbate.html')
    
    
    
    