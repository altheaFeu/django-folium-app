# django-folium-app
Application django qui affiche des communes et des hôpitaux sur une carte folium
Lien pour les communes : https://public.opendatasoft.com/explore/dataset/georef-france-commune/information/?flg=fr-fr&disjunctive.reg_name&disjunctive.dep_name&disjunctive.arrdep_name&disjunctive.ze2020_name&disjunctive.bv2022_name&disjunctive.epci_name&disjunctive.ept_name&disjunctive.com_name&disjunctive.ze2010_name&disjunctive.com_is_mountain_area
Lien pour les hôpitaux : https://babel.opendatasoft.com/explore/dataset/osm-fr-lieux-de-soin/export/

Je me suis basé pour ce projet d'une base de donnée postgre nommé foliumapp qui comportait 2 tables : 
1/ Une table nommée georef_france_commune avec les données communes
2/ Une table nommée hopitaux avec les données des hôpitaux.
