from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('roman', 'Roman'),
    ('histoire', 'Histoire'),
    ('philosophie', 'Philosophie'),
    ('sciences', 'Sciences'),
    ('economie', 'Économie'),
    ('informatique', 'Informatique'),
    ('medecine', 'Médecine'),
    ('poesie', 'Poésie'),
    ('theatre', 'Théâtre'),
    ('essai', 'Essai'),
    ('biographie', 'Biographie'),
    ('bd', 'Bande Dessinée'),
]

LANGUES = [
    ('fr', 'Français'),
    ('en', 'Anglais'),
]

class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, blank=True)
    annee_edition = models.IntegerField(null=True, blank=True)
    maison_edition = models.CharField(max_length=200, blank=True)
    langue = models.CharField(max_length=5, choices=LANGUES, default='fr')
    categories = models.CharField(max_length=200, help_text="Sépare les catégories par des virgules, ex: roman,histoire")
    resume = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    
    # Images
    couverture_avant = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    couverture_arriere = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    premiere_page = models.ImageField(upload_to='pages/', blank=True, null=True)

    def get_categories_list(self):
        return [c.strip() for c in self.categories.split(',')]

    def __str__(self):
        return self.titre

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.livre.disponible = False
        self.livre.save()
        super().save(*args, **kwargs)