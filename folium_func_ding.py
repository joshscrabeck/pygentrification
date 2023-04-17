# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 18:28:49 2023

@author: tul54884
"""

import pandas as pd
import folium as f
import geopandas as gpd
import webbrowser
import random




result_df = gpd.read_file('C:/Users/tul54884/Documents/gus_8066_scratch/dummydata.geojson')
#%% 
#readopting dummydataset for testing

result_df['gent_status'] = random.choices(['Nongentrifiable', 'No gentrification', 'Weak Gentrification', 'Moderate Gentrification', 'Intense Gentrification'],
                                          k = 408)
result_df['crit'] = random.choices([0,1,1.5,2,2.5,3,3.5,4], k=408)
result_df['gentrifying'] = random.choices([True, False], k = 408)

#%%
#defining folium function to be nested in ding function, will show 2 layers of results. The first a binary of
# gentrifying with a pop up denoting the criteria score calculated in Ding. Second layer shows the more detailed 
# gentrification classifications used in Ding paper

#ding_result_map(result_df = output)
def ding_result_map(result_df):
    
    
# style functions to color the two layers
    def gent_status_color(feature):
        if feature['properties']['gent_status']== 'Nongentrifiable':
            return '#938f8f'
        elif feature['properties']['gent_status']== 'No gentrification':
            return 'white'
        elif feature['properties']['gent_status']== 'Weak Gentrification':
            return '#ffffbf'
        elif feature['properties']['gent_status']== 'Moderate Gentrification':
            return '#fdae61'
        elif feature['properties']['gent_status']== 'Intense Gentrification':
            return '#d7191c'
        
    def gentrifying_color(feature):
        if feature ['properties']['gentrifying']== True :
            return '#fdae61'
        else:
            return 'white'
        
    
    
#creating a map object along with a basemap to add to it
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
    
# using feature groups for more control over layer control and display, adding the two data layers dependent on
# derived columns from the ding calculations, gent_status and gentrifying

    layer_fg = f.FeatureGroup(name='gentrifying', show = True, overlay= False)
    
    layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip = f.GeoJsonTooltip(fields= ['crit']),
        style_function = lambda feature: {'color': 'gray',
                                          'fillColor': gentrifying_color(feature),
                                          'fillOpacity':0.5,
                                          'weight':.3},
        name = 'gentrifying'
        ))
            
    layer2_fg = f.FeatureGroup(name='gentrification status', show= True, overlay= False)
    
    layer2_fg.add_child(f.GeoJson(
        result_df,
        tooltip = f.GeoJsonTooltip(fields= ['gent_status']),
        style_function = lambda feature: {'color': 'gray',
                                          'fillColor':gent_status_color(feature),
                                          'fillOpacity':0.4,
                                          'weight':.3},
        name = 'Gentrification Status(detailed)'
        ))
    
# adding the layers and a layer control to the map object and returning it as the output of the function

    layer_fg.add_to(m)
    layer2_fg.add_to(m)
    f.LayerControl().add_to(m)
    
    return m

#%%


ding_result_map(result_df).save('test.html')


webbrowser.open("test.html")
