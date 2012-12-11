# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from project.chercheurs.api import API
from project.chercheurs.forms import ChercheurSearchForm

def liste_chercheurs(request):               
    """ Liste des chercheurs """
    search_form = ChercheurSearchForm(request.GET)
    search_form.save(commit=False)
    
    api = API(request)    
    if not request.GET or request.GET.get('page') or request.GET.get('tri'):
        chercheurs = api.chercheurs_liste()
    else:
        chercheurs = api.chercheurs_recherche()

    if chercheurs is None:
        return render_to_response("chercheurs/erreur_sep_indisponible.html", {}, RequestContext(request))
    
    sort = request.GET.get('tri')
    
    if sort is not None and sort.endswith('_desc'):
        sort = sort[:-5]
        sens = True
    else:
        sens = False
    
    
    if sort == 'nom':
        chercheurs = sorted(chercheurs, key=lambda chercheur: chercheur.nom, reverse=sens)
    elif sort == 'etablissement':
        chercheurs = sorted(chercheurs, key=lambda chercheur: chercheur.etablissement, reverse=sens)
    elif sort == 'pays':
        chercheurs = sorted(chercheurs, key=lambda chercheur: chercheur.pays, reverse=sens)
   
    nb_chercheurs = len(chercheurs)

    c = {
        'chercheurs': chercheurs,
        'nb_chercheurs': nb_chercheurs,
        'search_form': search_form,
    }
    return render_to_response("chercheurs/liste_chercheurs.html", Context(c), context_instance = RequestContext(request))

def chercheur(request, chercheur_id):
    """ Détails d'un chercheur """
    api = API(request)
    chercheur = api.chercheur(chercheur_id)
    
    if not chercheur:
        return render_to_response("chercheurs/erreur_sep_indisponible.html", {}, RequestContext(request))

    c = {
        'chercheur': chercheur
    }
    return render_to_response("chercheurs/fiche.html", Context(c), context_instance = RequestContext(request))

