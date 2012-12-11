# -*- encoding: utf-8 -*

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed

from rigl.models import Actualite

class RecentActualiteFeed(Feed):
    title = "Réseau Interuniversitaire des Grands Lacs | Actualités récentes"
    description = "Atualités récentes du Réseau Interuniversitaire des Grands Lacs"
    #description_template = 'actu_description.html'

    def link(self):
        return reverse('rss_actualites')

    def items(self):
        return Actualite.objects.filter(active=True).order_by('-date_saisie')[:10]
    
    def item_title(self, item):
        return item.titre
    
    def item_description(self, item):
        return item.contenue
