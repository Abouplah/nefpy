# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('chercheurs.views',
    url(r'^$', 'liste_chercheurs',
        name='liste_chercheurs'),
    url(r'^(?P<chercheur_id>\w+)/$', 'chercheur',
        name='chercheur'),
)
