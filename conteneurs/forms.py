from django import forms
from .models import Conteneur


class ConteneurForm(forms.ModelForm):
    class Meta:
        model = Conteneur
        fields = ['nom', 'taille', 'etat']
        widgets = {
            'nom': forms.TextInput(attrs={
                'placeholder': 'Ex: MSCU1234567',
                'class': 'form-control',
                'style': 'text-transform: uppercase;'
            }),
            'taille': forms.Select(attrs={'class': 'form-control'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nom(self):
        # On force en majuscules avant validation, au cas où l'agent tape en minuscules
        return self.cleaned_data['nom'].upper()