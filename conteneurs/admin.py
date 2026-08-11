from django.contrib import admin
from .models import Conteneur, Emplacement


@admin.register(Conteneur)
class ConteneurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'taille', 'etat', 'statut', 'date_entree', 'date_sortie')
    list_filter = ('taille', 'etat', 'statut')
    search_fields = ('nom',)
    readonly_fields = ('date_entree',)


@admin.register(Emplacement)
class EmplacementAdmin(admin.ModelAdmin):
    list_display = ('code', 'zone', 'rangee', 'position', 'conteneur', 'est_occupe')
    list_filter = ('zone', 'rangee')
    search_fields = ('zone',)