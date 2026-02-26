from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Livre, CATEGORIES, LANGUES

def connexion(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
        else:
            error = "Identifiants incorrects"
    return render(request, 'bibliotheque/login.html', {'error': error})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def accueil(request):
    return render(request, 'bibliotheque/accueil.html')

@login_required
def liste_livres(request):
    langue = request.GET.get('langue', '')
    categorie = request.GET.get('categorie', '')
    recherche = request.GET.get('q', '')

    livres = Livre.objects.all()
    if langue:
        livres = livres.filter(langue=langue)
    if recherche:
        livres = livres.filter(titre__icontains=recherche)
    if categorie:
        livres = [l for l in livres if categorie in l.get_categories_list()]

    # Grouper par catégorie
    livres_par_categorie = {}
    for livre in livres:
        for cat in livre.get_categories_list():
            if not categorie or cat == categorie:
                livres_par_categorie.setdefault(cat, []).append(livre)

    return render(request, 'bibliotheque/liste_livres.html', {
        'livres_par_categorie': livres_par_categorie,
        'categories': CATEGORIES,
        'langues': LANGUES,
        'langue_filtre': langue,
        'categorie_filtre': categorie,
        'recherche': recherche,
    })

@login_required
def detail_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    return render(request, 'bibliotheque/detail_livre.html', {'livre': livre})