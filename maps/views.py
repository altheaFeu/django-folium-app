from django.contrib.gis.db.models.functions import AsGeoJSON
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .forms import RegionForm
import folium
from folium.plugins import MarkerCluster, Draw, MiniMap, Fullscreen, LocateControl
import geopandas as gpd
import pandas as pd
import json, h3
import uuid
from shapely.geometry import Polygon
from .models import Commune, Hopitaux

# Cache la page pendant 15 minutes pour éviter des requêtes fréquentes
@cache_page(60 * 15)
def home(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            reg_name = form.cleaned_data['regions']
            resolution = form.cleaned_data['resolution']

            # Utilisez le cache pour stocker les résultats de la requête
            key = f"home_data_{reg_name}_{resolution}"
            data = cache.get(key)
            if data is None:
                liste_com, liste_hopitaux = query_data(reg_name)
                x, y, hexagons, hexagons_ids = get_center_region(liste_com, resolution)
                m = create_map(y, x, 7)
                add_values_to_map(liste_com, liste_hopitaux, hexagons, hexagons_ids, m, form)
                add_control(m)

                # Stockez les données dans le cache
                data = {'map': m._repr_html_()}
                cache.set(key, data)

            return JsonResponse(data)
    else:
        form = RegionForm()

    m = create_map(46.227638, 2.213749, 5)
    add_control(m)

    context = {'map': m._repr_html_(), 'form': form}

    return render(request, 'maps/home.html', context)

# Crée la carte initiale avec l'emplacement et le zoom spécifiés
def create_map(latitude, longitude, zoom):
    m = folium.Map(location=[latitude, longitude],
                   zoom_start=zoom,
                   control_scale=True)

    # Ajout des plugins
    Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(m)
    
    Draw(position='topleft').add_to(m)
    MiniMap(toggle_display=True, zoom_level_offset=-5, position="topleft").add_to(m)

    return m

# Ajoute les contrôles à la carte, y compris les calques de tuiles, le contrôle de calque et le contrôle de localisation
def add_control(m):
    folium.TileLayer("OpenStreetMap").add_to(m)
    folium.TileLayer("cartodbpositron", show=False).add_to(m)
    folium.LayerControl().add_to(m)

    LocateControl().add_to(m)

# Effectue la requête pour obtenir les données des communes et des hôpitaux
def query_data(reg_name):
    communes_data = (
        Commune.objects
        .filter(reg_name__icontains=reg_name)
        .annotate(geojson=AsGeoJSON('geom'))
        .values('reg_name', 'geojson', 'dep_name', 'com_name', 'com_code')
    )

    hopitaux_data = (
        Hopitaux.objects
        .filter(reg_name__icontains=reg_name)
        .annotate(geojson=AsGeoJSON('wkb_geometry'))
        .values('name', 'geojson', 'amenity')
    )

    return communes_data, hopitaux_data

# Obtient le point central de la région et les hexagones correspondants
def get_center_region(liste_com, resolution):
    liste_geojson = [commune['geojson'] for commune in liste_com]
    gdfs = [gpd.read_file(geojson) for geojson in liste_geojson]
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
    center_point = merged_gdf.unary_union.centroid
    
    hexagons, hexagon_ids = create_hex(center_point.x, center_point.y, resolution, merged_gdf)
    
    return center_point.x, center_point.y, hexagons, hexagon_ids

# Ajoute les données des communes, des hôpitaux et des hexagones à la carte
def add_values_to_map(communes_data, hopitaux_data, hexagons, hexagon_ids, m, form):
    couleur = form.cleaned_data['couleur']
    couleur_hopitaux = form.cleaned_data['couleur_hopitaux'] 
    couleur_h3 = form.cleaned_data['couleur_h3']   
     
    transparence = form.cleaned_data['transparence']
    transparence_h3 = form.cleaned_data['transparence_h3']
    
    groupe_communes = folium.FeatureGroup(name="Communes")
    marker_hopitaux = MarkerCluster(name='Hopitaux')
    groupe_hexagones = folium.FeatureGroup(name="Hexagones")

    for commune in communes_data:
        folium.GeoJson(commune['geojson'], 
                        name=commune['reg_name'], 
                        style_function=lambda feature: {
                            "fillOpacity": transparence,
                            "fillColor": couleur,
                            "color": "black",
                            "dashArray": "5,5",
                            "weight": "0.5",
                        },
                        tooltip=f"<p><strong>Commune :</strong> {commune['com_name']}<br><strong>Code :</strong> {commune['com_code']}</p>",
                        smooth_factor=2.0,  
        ).add_to(groupe_communes)

    for hopital in hopitaux_data:
        geojson_dict = json.loads(hopital['geojson'])
        lat, lon = geojson_dict['coordinates'][1], geojson_dict['coordinates'][0]
        folium.Marker(
            location=[lat, lon],
            popup=f"<div style='width: 200px;'><p><strong>Nom :</strong> {hopital['name']}<br><strong>Aménité :</strong> {hopital['amenity']}<br><strong>Latitude :</strong> {lat}<br><strong>Longitude :</strong> {lon}</p></div>",
            icon=folium.Icon(color=couleur_hopitaux),
        ).add_to(marker_hopitaux)
        
    for idx, hexagon in enumerate(hexagons):
        hexagon_id = hexagon_ids[idx]
        folium.GeoJson(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [list(hexagon.exterior.coords)]
                },
                "properties": {"id": hexagon_id}
            },
            style_function=lambda feature: {
                "fillOpacity": transparence_h3,
                "fillColor": couleur_h3,
                "color": "black",
                "weight": "0.2",
            },
        ).add_to(groupe_hexagones)

    groupe_communes.layer_name = "Communes"
    marker_hopitaux.layer_name = "Hôpitaux"
    groupe_hexagones.layer_name = "Hexagones"

    groupe_communes.add_to(m)
    marker_hopitaux.add_to(m)
    groupe_hexagones.add_to(m)
    
# Crée des hexagones autour du point central avec une résolution spécifiée
def create_hex(center_x, center_y, resolution, merged_gdf):
    center_hexagon = h3.geo_to_h3(center_y, center_x, resolution)
    
    radius = 20
    
    hexagons = h3.k_ring(center_hexagon, radius)
    
    hexagon_polygons = [Polygon(h3.h3_to_geo_boundary(hexagon, True)) for hexagon in hexagons]
    
    filtered_hexagons = [hexagon for hexagon in hexagon_polygons if any(merged_gdf.intersects(hexagon))]
    
    # Ajoutez les identifiants aux hexagones
    hexagon_ids=[]
    hexagon_ids.extend(str(uuid.uuid4()) for _ in range(len(filtered_hexagons)))
    
    return filtered_hexagons, hexagon_ids
