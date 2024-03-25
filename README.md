# Application django des hôpitaux par région 🏥

[![Django](https://img.shields.io/badge/Django-3.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.1.1-orange.svg)](https://postgis.net/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.4-blue.svg)](https://www.postgresql.org/)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen.svg)](LICENSE.md)
[![Build By](https://img.shields.io/badge/Build%20By-Althéa_Feuillet-orange.svg)](https://yourportfolio.com)
[![En Cours de Modification](https://img.shields.io/badge/En%20Cours%20de%20Modification-Oui-green.svg)](LICENSE.md)

## Introduction
A partir d'une région sélectionnée, cette application affiche sur une carte folium : 
- Les hopitaux de la région
- Les communes de la région
- Un pavé d'hexagone avec la résolution 

L'application se base sur une base de données PostgreSQL nommée foliumapp, contenant deux tables principales : georef_france_commune pour les données des communes et hopitaux pour les données des hôpitaux.

## Sources de données

Les données utilisées dans cette application proviennent des sources suivantes :

- Données des communes : [OpenDataSoft](https://public.opendatasoft.com/explore/dataset/georef-france-commune/information/?flg=fr-fr&disjunctive.reg_name&disjunctive.dep_name&disjunctive.arrdep_name&disjunctive.ze2020_name&disjunctive.bv2022_name&disjunctive.epci_name&disjunctive.ept_name&disjunctive.com_name&disjunctive.ze2010_name&disjunctive.com_is_mountain_area)
- Données des hôpitaux : [OpenDataSoft](https://babel.opendatasoft.com/explore/dataset/osm-fr-lieux-de-soin/export/)

## Installation

Pour utiliser cette application, suivez ces étapes :

1. Assurez-vous d'avoir Python et Django installés sur votre système.
2. Clonez ce dépôt dans votre environnement de développement.
3. Installez les dépendances en exécutant `pip install -r requirements.txt`.
4. Assurez-vous que PostgreSQL est installé et configurez la base de données comme décrit dans la section suivante.
5. Lancez le serveur Django avec la commande `python manage.py runserver`.

## Configuration de la base de données

Avant de lancer l'application, vous devez créer la base de donnée PostgreSQL.  

Pour créer la base de données PostgreSQL avec PostGIS, importer les données des communes et des hôpitaux, créer les tables correspondantes et ajouter un index spatial à chaque table.

### 1. Création de la base de données et des tables

Ouvrez une interface de commande et connectez-vous à votre serveur PostgreSQL en tant qu'utilisateur ayant les privilèges nécessaires.Ensuite, créez une nouvelle base de données nommée `foliumapp` :

```sql
CREATE DATABASE foliumapp;
CREATE EXTENSION postgis;
```

### 2. Importation des données

Télécharger les données et importer les tables dans la console !:

```bash
psql -U postgres -d foliumapp -c "COPY georef_france_commune FROM 'nom_du_fichier.csv' WITH CSV HEADER DELIMITER ';';"

ogr2ogr -f "PostgreSQL" PG:"dbname=foliumapp user=postgres" chemin_vers_le_fichier.geojson -nln hopitaux -nlt PROMOTE_TO_MULTI
```

### 4. Ajout d'un index spatial

Après avoir importé les données, vous pouvez ajouter un index spatial à chaque table pour optimiser les performances des requêtes spatiales.

```sql
CREATE INDEX idx_georef_france_commune_geom ON georef_france_commune USING GIST(geom);
CREATE INDEX idx_hopitaux_geom ON hopitaux USING GIST(wkb_geometry);
```

### 5. Configuration de la base de données dans le README

Ajoutez les informations suivantes dans la section "Configuration de la base de données" du README :

```markdown
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'foliumapp',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Assurez-vous de remplacer `'votre_utilisateur'` et `'votre_mot_de_passe'` par les informations de connexion appropriées.

## Utilisation

Une fois l'application lancée, vous pouvez accéder à la carte interactive en ouvrant votre navigateur et en visitant l'URL fournie par le serveur Django, généralement `http://localhost:8000/`.

Sur la carte, vous pouvez sélectionner une région à partir du formulaire et personnaliser l'apparence des communes et des hôpitaux en ajustant les paramètres.

