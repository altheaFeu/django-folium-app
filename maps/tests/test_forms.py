from django.test import TestCase
from src.maps.forms import RegionForm

class RegionFormTests(TestCase):
    def test_region_form_valid_data(self):
        # Testez le formulaire avec des données valides
        form_data = {
            'regions': 'Bourgogne-Franche-Comté',
            'couleur': '#D4B36A',
            'transparence': 0.8,
            'couleur_hopitaux': '#FF5733',
            'resolution': 3,
            'couleur_h3': '#FF5733',
            'transparence_h3': 0.8,
        }
        form = RegionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_region_form_invalid_data(self):
        # Testez le formulaire avec des données invalides
        form_data = {
            'regions': '',  # Champs requis manquant
            'couleur': '#D4B36A',
            'transparence': 0.8,
            'couleur_hopitaux': '#FF5733',
            'resolution': 3,
            'couleur_h3': '#FF5733',
            'transparence_h3': 0.8,
        }
        form = RegionForm(data=form_data)
        self.assertFalse(form.is_valid())
