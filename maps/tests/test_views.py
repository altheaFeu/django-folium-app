from django.test import TestCase
from django.urls import reverse
from src.maps.models import Commune, Hopitaux
from src.maps.views import home 

class HomeViewTests(TestCase):
    def setUp(self):
        # Créez des objets Commune et Hopitaux pour les tests
        Commune.objects.create(reg_name='TestRegion', com_name='TestCommune', com_code='12345')
        Hopitaux.objects.create(reg_name='TestRegion', name='TestHospital', amenity='Hospital')

    def test_home_view_with_valid_data(self):
        # Testez la vue home avec des données valides en utilisant la méthode POST
        form_data = {'regions': 'TestRegion', 'resolution': 3}
        response = self.client.post(reverse('home'), data=form_data)

        self.assertEqual(response.status_code, 200)
        
    def test_home_view_with_invalid_data(self):
        # Testez la vue home avec des données invalides en utilisant la méthode POST
        form_data = {'regions': 'InvalidRegion', 'resolution': 3}
        response = self.client.post(reverse('home'), data=form_data)

        self.assertEqual(response.status_code, 200)

    def test_home_view_with_get_request(self):
        # Testez la vue home avec une requête GET
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
