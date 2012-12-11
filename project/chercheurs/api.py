#-*- encoding: utf-8 -*

import urllib
from django.utils import simplejson
from django.conf import settings

from restkit import request


def req(url):
    if settings.DEBUG:
        print url    
    r = request(url)
    if r.status_int not in (200, ):
        raise Exception("can't reach url :%s\n%s" % (url, r.status))
    return r

class API:
    def __init__(self, request):
        self.request = request
        self.env = settings.ENV

    def chercheurs_recherche(self):
        chercheurs = []
        q = self.request.GET.get('q')
        if 'etablissement_libre' in self.request.GET:
            q += " %s" % self.request.GET.get('etablissement_libre')

        # encore('utf-8') est utilisé pour éviter les problèmes d'encodage de l'URL
        filtres = {
                'q': q.encode('utf-8'),
                'nom_chercheur': self.request.GET.get('nom_chercheur').encode('utf-8'),
                'domaine': self.request.GET.get('domaine'),
                'statut': self.request.GET.get('statut'),
                'discipline': self.request.GET.get('discipline'),
                'pays': self.request.GET.get('pays'),
                'activites_francophonie':
                    self.request.GET.get('activites_francophonie'),
                'genre': self.request.GET.get('genre'),
                'limitation_pays': u','.join(settings.PAYS_SOUS_REGION),
                }

        params = urllib.urlencode(filtres)
        url = "%s?%s" % (settings.SEP_URLS[self.env] + "recherche/", params)
        try:
            r = req(url)
            data = r.body_string()
            chercheurs_json = simplejson.loads(data)
            
            for c in chercheurs_json:
                chercheur = type('Chercheur', (object,), {
                'id' : c['id'],
                'prenom' : c['prenom'],
                'nom' : c['nom'],
                'etablissement' : c['etablissement'],
                'etablissement_autre_nom' : c['etablissement'],
                'pays' : c['pays'],
                'etablissement_pays_autre_nom' : c['etablissement']})
                chercheurs.append(chercheur)
        except Exception:
            chercheurs = None

        return chercheurs

    def chercheurs_liste(self):
        chercheurs = []

        url = settings.SEP_URLS[self.env] + "pays/%s/" % ','.join(settings.PAYS_SOUS_REGION)
        try:
            r = req(url)
            data = r.body_string()
            chercheurs_json = simplejson.loads(data)
            for c in chercheurs_json:
                chercheur = type('Chercheur', (object,), {
                'id' : c['id'],
                'prenom' : c['prenom'],
                'nom' : c['nom'],
                'etablissement' : c['etablissement'],
                'etablissement_autre_nom' : c['etablissement_pays_autre_nom'],
                'pays' : c['pays'],
                'etablissement_pays_autre_nom' : c['etablissement_pays_autre_nom']})
                chercheurs.append(chercheur)
        except Exception:
            chercheurs = None

        return chercheurs

    def chercheur(self, chercheur_id):
        url = settings.SEP_URLS[self.env] + "%s/" % chercheur_id
        try:
            r = req(url)            
            data = r.body_string()
            chercheur_json = simplejson.loads(data)
            chercheur = type('Chercheur', (object,), chercheur_json)
            if not chercheur is None:
                if not settings.PAYS_SOUS_REGION.__contains__(chercheur.pays_code):
                    chercheur = None
        except Exception:
            chercheur = False

        return chercheur
