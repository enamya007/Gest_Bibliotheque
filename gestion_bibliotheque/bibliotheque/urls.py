from django.urls import path
from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('accueil/', views.accueil, name='accueil'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/<int:pk>/', views.detail_livre, name='detail_livre'),
]