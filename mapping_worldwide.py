from encodings import utf_8, utf_8_sig
import folium as fl
import pandas as pd
from branca.element import Template, MacroElement

map = fl.Map(location= [32.679107, -115.198693127], zoom_start = 3, tiles ="Stamen Terrain", max_bounds= True, min_zoom= 2 )

volcanoes = pd.read_csv("worldwide_volcanoes.txt", sep =";", encoding= "ISO-8859-1")

lat = list(volcanoes["LAT"])
lon = list(volcanoes["LON"])
elev = list(volcanoes["ELEV"])
na = list(volcanoes["NAME"])

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
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
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 30px;'>
     
<div class='legend-title'>Volcano Elevation In Meters </div>
  <ul class='legend-labels'>
    <li><span style='background:green;opacity:0.7;'></span>Below 1000</li>
    <li><span style='background:purple;opacity:0.7;'></span>Below 2000</li>
    <li><span style='background:blue;opacity:0.7;'></span>Below 3000</li>
    <li><span style='background:orange;opacity:0.7;'></span>Below 4000</li>
    <li><span style='background:red;opacity:0.7;'></span>Above 4000</li>

  </ul>
</div>
 
</body>
</html>

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

macro = MacroElement()
macro._template = Template(template)

fg2 = fl.FeatureGroup(name = "Population")
fg1= fl.FeatureGroup(name = "Volcanoes")

def elevation_color(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 2000:
        return 'purple'
    elif  2000 <= elevation < 3000:
        return 'blue'
    elif 3000 <= elevation < 4000:
        return 'orange'
    else:
        return 'red'  

for lt, ln, nm, el in zip(lat , lon, na, elev):
    fg1.add_child(fl.CircleMarker(location = [lt, ln], radius = 7,
     tooltip= nm + " , Elevation:" + str(el) + " m", fill = True, fill_color = elevation_color(el), fill_opacity = 1, weight = .1))

map.add_child(fg1)

fg2.add_child(fl.GeoJson(data = open("world.json", mode = 'r', encoding = 'utf-8-sig').read(), 
    style_function= lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
    else 'blue' if 10000000 <= x["properties"]["POP2005"] < 50000000 
    else 'yellow' if 50000000 <= x["properties"]["POP2005"] < 100000000
    else 'red' }))

map.add_child(fg2)

map.add_child(fl.LayerControl(position = "topleft", hideSingleBase = True ))

map.add_child(macro)

map.save("Volcanoes_and_Population_Map.html")
