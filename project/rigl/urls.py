# -*- encoding: utf-8 -*


from django.conf.urls.defaults import patterns, url
from rigl.feeds import RecentActualiteFeed



urlpatterns = patterns('rigl.views',
    #Site principal
    url(r'^$', 'home', name='home'),
    url(r'^toutes_actualites/$', 'toutes_actualites', name='toutes_actualites'),
    url(r'^actualite/(?P<actualite_id>\d+)/$', 'detail_actualites', name='detail_actualites'),
    url(r'^actualites/(?P<categorie_slug>\w+)/$', 'actualites', name='actualites'),
    
    
    url(r'^rss/actualites$', RecentActualiteFeed(), name='rss_actualites'),
)
