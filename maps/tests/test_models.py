from django.test import TestCase
from src.maps.models import Commune, Hopitaux

class CommuneModelTests(TestCase):
    def test_commune_model_str_representation(self):
        # Testez la représentation en chaîne du modèle Commune
        commune = Commune(reg_name='TestRegion', com_name='TestCommune', com_code='12345')
        self.assertEqual(str(commune), 'TestRegion')

class HopitauxModelTests(TestCase):
    def test_hopitaux_model_str_representation(self):
        # Testez la représentation en chaîne du modèle Hopitaux
        hopital = Hopitaux(reg_name='TestRegion', name='TestHospital', amenity='Hospital')
        self.assertEqual(str(hopital), 'TestRegion')