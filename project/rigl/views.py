# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Categorie, Actualite

#def home(request):
#    """Page d'accueil du site"""
#    c = {
#    }
#    return render_to_response("home.html", Context(c), context_instance = RequestContext(request))

def home(request):
    """ Actualité défilant: les quatre derniers actualités insérés """ 
    actualite_def = Actualite.objects.\
                filter(active=True).\
                filter(defilante=True).\
                order_by('-date_saisie')
    """ Actualté de la page d'accueil: Affihe uniqement l'image et le titre  """
    actualite = Actualite.objects.\
                filter(active=True).\
                order_by('-date_saisie')
    variables = RequestContext(request, {
        'atualite_defilantes': actualite_def,
        'actualites': actualite,
    })
    return render_to_response("home.html", variables)
    

""" Affiche toutes l'actualités: titre et resumé dans une page. """
def toutes_actualites(request):
    all_actu = Actualite.objects.\
            filter(active=True).\
            order_by('-date_saisie')
    variables = RequestContext(request, {
        'actualites': all_actu,
    })
    return render_to_response("toutes_actualites.html", variables)
    
    """ Affiche une actualité conplet: titre, resumé, et contenu dans une page. """
def detail_actualites(request, actualite_id):    
    #actualite = Actualite.objects.filter(pk=id)
    actualite = get_object_or_404(Actualite, pk=actualite_id)
    variables = RequestContext(request, {
      'actualite': actualite,
    })
    return render_to_response("actualite.html", variables)
    

# Test de fusion

def actualites(request, categorie_slug):    
    #Actualité de RIGL uniquement; pour le menu horizontal
    actualite_rigl = Actualite.objects.\
        filter(active=True).\
        filter(categorie__slug__icontains=categorie_slug).\
        order_by('-date_saisie')
    variables = RequestContext(request, {
      'actualites': actualite_rigl,
    })
    return render_to_response("actualite_precise.html", variables)



