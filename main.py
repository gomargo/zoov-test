import os.path
import folium
import json

from branca.element import Template, MacroElement

# création map centrée sur la France métropolitaine
m = folium.Map(location=[46.6211319, 2.1605771],
               zoom_start=7,
               tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
               attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')

# rattachement du fichier json à folium
nodeData = os.path.join('centres_vaccination.json')

file = "./centres_vaccination.json"

g = folium.GeoJson(
    file,
    name="centres_vaccination"
).add_to(m)

# reading JSON file
with open('centres_vaccination.json') as access_json:
    read_content = json.load(access_json)

feature_access = read_content['features']

feature_group = folium.FeatureGroup(name='popup')

# création d'un popup quand on clique sur le marker
geo_json = folium.GeoJson(nodeData)

# Faire apparaitre certaines informations nom du centre dans le popup, pour chaque ligne on prend le champ properties
# et on prend la propriété 'c_nom'
for feature_data in feature_access:
    buildingName = feature_data['properties']
    c_nom = buildingName['c_nom']
    geo_json.add_child(folium.Popup(str(c_nom)))

#le popup correspond à la dernière entrée du Json, j'ai essayé d'utiliser la nouvelle fonction GeoJson Popup mais
#il n'y a rien qui s'affiche
#geo_json = folium.GeoJson(nodeData, popup=folium.GeoJsonPopup(["c_nom"]))

geo_json.add_to(m)

# rajout d'un encart pour illustrer la map
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
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

<div class='legend-title'>Carte des centres de vaccinations contre le covid 19<br> en France métropolitaine et 
territoires d'outre-mer </div>
<div class='legend-scale'>

</div>
</div>

</body>
</html>
<style type='text/css'>
  .maplegend .legend-title {
    text-align: center;
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

m.get_root().add_child(macro)

geo_json.add_to(m)

# sauvegarde dans un fichier index.hatml
m.save("index.html")
