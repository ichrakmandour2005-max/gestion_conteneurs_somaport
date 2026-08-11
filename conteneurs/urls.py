from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plan/', views.plan_parc, name='plan_parc'),
    path('conteneurs/', views.liste_conteneurs, name='liste_conteneurs'),
    path('conteneurs/ajouter/', views.ajouter_conteneur, name='ajouter_conteneur'),
    path('conteneurs/sortir/<int:conteneur_id>/', views.sortir_conteneur, name='sortir_conteneur'),
    path('conteneurs/transferer/<int:conteneur_id>/', views.transferer_conteneur, name='transferer_conteneur'),
    path('duree-sejour/', views.duree_sejour, name='duree_sejour'),
    path('historique/', views.historique, name='historique'),
    path('duree-sejour/export/', views.export_duree_sejour, name='export_duree_sejour'),
]