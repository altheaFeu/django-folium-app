from django import forms

# Formulaire utilisé pour collecter les paramètres de la région et de la carte
class RegionForm(forms.Form):
    # Champ de sélection pour choisir une région parmi les options
    regions = forms.ChoiceField(choices=[
        ('Bourgogne-Franche-Comté', 'Bourgogne-Franche-Comté'),
        ('Auvergne-Rhône-Alpes', 'Auvergne-Rhône-Alpes'),
        ('Normandie', 'Normandie'),
        ('Hauts-de-France', 'Hauts-de-France'),
        ('Grand Est', 'Grand Est'),
        ('Occitanie', 'Occitanie'),
        ('Nouvelle-Aquitaine', 'Nouvelle-Aquitaine'),
        ('Bretagne', 'Bretagne'),
        ('Centre-Val de Loire', 'Centre-Val de Loire'),
        ("Provence-Alpes-Côte d'Azur", "Provence-Alpes-Côte d'Azur"),
        ('Corse', 'Corse'),
        ('Pays de la Loire', 'Pays de la Loire'),
        ('Île-de-France', 'Île-de-France'),
    ],
    widget=forms.Select(attrs={'class': 'form-control'}))

    # Champ pour spécifier la couleur des communes avec un sélecteur de couleur
    couleur = forms.CharField(label='Couleur des communes', required=False, initial='#D4B36A',
                              widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control spectrum-colorpicker'}))

    # Champ pour régler la transparence des communes avec un curseur
    transparence = forms.FloatField(label='Transparence des communes', required=False, initial=0.8,
                                    widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.1', 'min': '0', 'max': '1',
                                                                  'class': 'form-range'}))

    # Champ pour spécifier la couleur des hôpitaux avec un sélecteur de couleur
    couleur_hopitaux = forms.CharField(label='Couleur des hôpitaux', required=False, initial='#FF5733',
                                       widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control spectrum-colorpicker'}))

    # Champ pour spécifier la résolution des hexagones avec un nombre entier
    resolution = forms.IntegerField(
        label='Résolution des hexagones',
        required=True,
        initial=3,
        widget=forms.NumberInput(attrs={'type': 'number', 'min': 1, 'max': 6, 'class': 'form-control'}),
    )

    # Champ pour spécifier la couleur des hexagones avec un sélecteur de couleur
    couleur_h3 = forms.CharField(label='Couleur des hexagones', required=False, initial='#FF5733',
                                 widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control spectrum-colorpicker'}))

    # Champ pour régler la transparence des hexagones avec un curseur
    transparence_h3 = forms.FloatField(label='Transparence des hexagones', required=False, initial=0.8,
                                       widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.1', 'min': '0', 'max': '1',
                                                                     'class': 'form-range'}))
