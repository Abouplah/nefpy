from django.conf.urls.defaults import *

urlpatterns = patterns(
    'auf.django.references.views',
    (r'^autocomplete/etablissements.json$', 'autocomplete_etablissements'),
    (r'^etablissements/(\d+).json$', 'etablissement_json'),
)
