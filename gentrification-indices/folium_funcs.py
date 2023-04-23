#Functions to create Folium maps from the output of the Bates-Freeman and Ding functions#

import folium as f
import branca

#%%

def ding_result_map(result_df, filename = 'ding_map.html'):
    ''' This function takes in the GeoDataFrame generated by the calc_ding function and outputs and map object of a Folium map. It saves an html file of the map object to the working directorand opens it in a web browser.
    
    Parameters
    -------------
    result_df: GeoDataFrame from ding function
    file_name: name for output html file. Default name is ding_map.html 

    Returns
    ------------
    Map object and html file
    
    References
    -------------
    https://python-visualization.github.io/folium/
     
      '''
    
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
    
# Creating a basic macro element to act as the legend(s) for the resulting layers for the Ding function
    
    template_ding = """
    {% macro html(this, kwargs) %}
    
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Gentrifying areas by Ding (2016) method </title>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    
      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
      
      <script>
      $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                                
                            });
                        }
                    });
    });
    
      </script>
      
      
      <script>
      $( function() {
        $( "#maplegend2" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });
    
      </script>
      
      
      
    </head>
    <body>
    
     
    <div id='maplegend' class='maplegend' 
        style='position: absolute; left: 82%; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
         
    <div class='legend-title'>Gentrification Status</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#938f8f;opacity:0.7;'></span>nongentrifiable</li>
        <li><span style='background:white;opacity:0.7;'></span>no gentrification</li>
        <li><span style='background:#ffffbf;opacity:0.7;'></span>weak gentrification</li>
        <li><span style='background:#fdae61;opacity:0.7;'></span>moderate gentrification</li>
        <li><span style='background:#d7191c;opacity:0.7;'></span>intense gentrification</li>
    
    
      </ul>
    </div>
    </div>
     
    
    <div id='maplegend2' class='maplegend2' 
        style='position: absolute; bottom: 50%; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 200px;'>
         
    <div class='legend-title'>Gentrifying</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#fdae61;opacity:0.7;'></span>gentrifying</li>
        <li><span style='background:white;opacity:0.7;'></span>no gentrification</li>

    
    
      </ul>
    </div>
    </div>
    
    
    
    
    </body>
    </html>
    
    
    <style type='text/css'>
      .maplegend2 .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend2 .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend2 .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend2 ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend2 .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend2 a {
        color: #777;
        }
    </style>
    
    <style type='text/css'>
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""
    
    
    macro_ding = branca.element.MacroElement()
    macro_ding._template = branca.element.Template(template_ding)
    
    layer2_fg.add_child(macro_ding)
    
    
    
    
# adding the layers and a layer control to the map object and returning it as the output of the function

    layer_fg.add_to(m)
    layer2_fg.add_to(m)
    f.LayerControl().add_to(m)
    
    m.save(filename)
    
    return m

#%%
def bates_freeman_result_map(result_df, filename = 'bates_freeman_map.html'):
    ''' This function takes in the GeoDataFrame generated by the calc_batesfreeman function fand outputs and map object of a Folium map. It saves an html file of the map object to the working directorand opens it in a web browser.
    
    Parameters
    -------------
    result_df: GeoDataFrame from calc_batesfreeman function
    file_name: name for output html file. Default name is ding_map.html 

    Returns
    ------------
    Map object and html file
    
    References
    -------------
    https://python-visualization.github.io/folium/
       
      '''
# style functions for the resulting layers from the bates freeman function

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

#creating basemap and display origin point for the bates freeman results
    
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
    
    
    dem_chg_layer_fg = f.FeatureGroup(name='Demographic Change Index', show = True, overlay= False)
    
    dem_chg_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip = f.GeoJsonTooltip(fields=['dem_change_index']),   #perhaps Winn wants a different popup value?
        style_function = lambda feature: {'color': 'gray',
                                          'fillColor': dem_change_index_color(feature),
                                          'fillOpacity':0.5,
                                          'weight':.3},
        name= 'Demographic Change Index'
        ))
    
    
    vuln_ind_layer_fg = f.FeatureGroup(name= 'Vulnerability Index', show= True, overlay= False)
    
    vuln_ind_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip= f.GeoJsonTooltip(fields= ['v_index']),
        style_function = lambda feature:{'color': 'gray',
                                         'fillColor': vuln_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight': .3},
        name = 'Vulnerability Index'
             ))
    
    
    
    house_typo_layer_fg = f.FeatureGroup(name = 'Housing Typology Index', show= True, overlay=False)
    
    house_typo_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip= f.GeoJsonTooltip(fields= ['mhv_type']),
        style_function= lambda feature: {'color': 'gray',
                                         'fillColor': housing_typology_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight':.3},
        name = 'Housing Typology Index'
            ))
    
    
    
    freeman_layer_fg = f.FeatureGroup(name= 'Freeman Index', show= True, overlay= False)
    
    freeman_layer_fg.add_child(f.GeoJson(
        result_df,
        tooltip=f.GeoJsonTooltip(fields= ['freeman']),
        style_function= lambda feature: {'color': 'gray',
                                         'fillColor': freeman_index_color(feature),
                                         'fillOpacity':0.5,
                                         'weight':.3},
        name= 'Freeman Index'
        ))

# creating a macro element to serve as the legends for the resulting map from the Bates Freeman function
    
    template_batesfreeman = """
    {% macro html(this, kwargs) %}
    
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Gentrifying areas by Bates/Freemen Indices </title>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    
      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
      
      <script>
      $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                                
                            });
                        }
                    });
    });
    
      </script>
      
      
      <script>
      $( function() {
        $( "#maplegend2" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });
    
      </script>
      
      
      <script>
      $( function() {
        $( "#maplegend3" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });
    
      </script>
      
      
      <script>
      $( function() {
        $( "#maplegend4" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });
    
      </script>
      
      
      
    </head>
    <body>
    
     
    <div id='maplegend' class='maplegend' 
        style='position: absolute; left: 82%; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
         
    <div class='legend-title'>Vulnerability Index Scores</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#fee5d9;opacity:0.7;'></span>0</li>
        <li><span style='background:#fcae91;opacity:0.7;'></span>1</li>
        <li><span style='background:#fb6a4a;opacity:0.7;'></span>2</li>
        <li><span style='background:#de2d26;opacity:0.7;'></span>3</li>
        <li><span style='background:#a50f15;opacity:0.7;'></span>4</li>
    
    
      </ul>
    </div>
    </div>
     
    
    <div id='maplegend2' class='maplegend2' 
        style='position: absolute; bottom: 50%; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 200px;'>
         
    <div class='legend-title'>Demographic Change Index</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:orange;opacity:0.7;'></span>True</li>
        <li><span style='background:white;opacity:0.7;'></span>False</li>

    
    
      </ul>
    </div>
    </div>
    
    
    <div id='maplegend3' class='maplegend3' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; left: 20px; bottom: 20px;'>
         
    <div class='legend-title'>Freeman Index Scores</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:white;opacity:0.7;'></span>0</li>
        <li><span style='background:#bdd7e7;opacity:0.7;'></span>1</li>
        <li><span style='background:#6baed6;opacity:0.7;'></span>2</li>
        <li><span style='background:#3182bd;opacity:0.7;'></span>3</li>
        <li><span style='background:#08519c;opacity:0.7;'></span>4</li>
    
    
      </ul>
    </div>
    </div>
    
    
    
    <div id='maplegend4' class='maplegend4' 
        style='position: absolute; left: 82%; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; left: 20px; bottom: 200px;'>
         
    <div class='legend-title'>Housing Typology Index</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#white;opacity:0.7;'></span>no typology</li>
        <li><span style='background:#fde0dd;opacity:0.7;'></span>adjacent</li>
        <li><span style='background:#fa9fb5;opacity:0.7;'></span>accelerating</li>
        <li><span style='background:#c51b8a;opacity:0.7;'></span>appreciated</li>
    
    
      </ul>
    </div>
    </div>
    
    
    
    
    </body>
    </html>
    
    
    <style type='text/css'>
      .maplegend2 .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend2 .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend2 .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend2 ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend2 .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend2 a {
        color: #777;
        }
    </style>
    
    <style type='text/css'>
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    
    
    
    
    <style type='text/css'>
      .maplegend3 .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend3 .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend3 .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend3 ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend3 .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend3 a {
        color: #777;
        }
    </style>
    
    
    <style type='text/css'>
      .maplegend4 .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend4 .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend4 .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend4 ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend4 .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend4 a {
        color: #777;
        }
    </style>
    
    
    {% endmacro %}"""
    
    
    macro_bates = branca.element.MacroElement()
    macro_bates._template = branca.element.Template(template_batesfreeman)
    
    freeman_layer_fg.add_child(macro_bates)
    
    
    
    
    
    
    
    freeman_layer_fg.add_to(m)
    house_typo_layer_fg.add_to(m)
    vuln_ind_layer_fg.add_to(m)
    dem_chg_layer_fg.add_to(m)
    f.LayerControl().add_to(m)
    
    m.save(filename)
    
    return m


