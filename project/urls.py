# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from rigl.feeds import RecentActualiteFeed


from ajax_select import urls as ajax_select_urls

admin.autodiscover()

handler404
handler500 # Pyflakes

feed_setup = {
  'actualite': RecentActualiteFeed,
}

urlpatterns = patterns('',

    #Site principal
    url(r'^', include('rigl.urls')),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Chercheurs
    (r'^lookups/', include(ajax_select_urls)),

    # CMS
    url(r'^', include('cms.urls')),
    
     # Feeds
    url(r'^latest/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
                        {'feed_dict': feed_setup}, ),
    
   
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
