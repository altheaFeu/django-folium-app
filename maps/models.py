from django.contrib.gis.db import models

# Modèle de données pour représenter une commune
class Commune(models.Model):
    id = models.AutoField(primary_key=True)
    reg_name = models.CharField(max_length=255)
    dep_name = models.CharField(max_length=255, default='Inconnu')
    com_name = models.CharField(max_length=255, default='Inconnu')
    com_code = models.CharField(max_length=255, default='Inconnu')
    geom = models.GeometryField(null=True, blank=True)

    class Meta:
        db_table = 'georef_france_commune'  # Nom de la table dans la base de données

    def __str__(self):
        return self.reg_name  # Représentation en chaîne du modèle, renvoie le nom de la région

# Modèle de données pour représenter un hôpital
class Hopitaux(models.Model):
    id = models.AutoField(primary_key=True)
    reg_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amenity = models.CharField(max_length=255)
    wkb_geometry = models.PointField(null=True, blank=True)

    class Meta:
        db_table = 'hopitaux'  # Nom de la table dans la base de données

    def __str__(self):
        return self.reg_name  # Représentation en chaîne du modèle, renvoie le nom de la région
