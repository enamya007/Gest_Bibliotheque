from django.contrib import admin
from .models import Auteur, Livre, Etudiant, Emprunt

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'langue', 'annee_edition', 'disponible']
    list_filter = ['langue', 'disponible']
    search_fields = ['titre', 'auteur__nom']

admin.site.register(Auteur)
admin.site.register(Etudiant)
admin.site.register(Emprunt)