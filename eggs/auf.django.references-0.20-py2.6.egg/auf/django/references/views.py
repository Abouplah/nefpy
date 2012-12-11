from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson

from auf.django.references import models as ref

def autocomplete_etablissements(request):
    term = request.GET.get('term')
    exclude_refs = request.GET.get('exclude_refs')
    include = request.GET.get('include')
    if term:
        etablissements = ref.Etablissement.objects.filter(nom__icontains=term)
        if exclude_refs:
            q = Q(**{str(exclude_refs): None})
            if include:
                q |= Q(id=include)
            etablissements = etablissements.filter(q)
        pays = request.GET.get('pays')
        if pays:
            etablissements = etablissements.filter(pays=pays)
            result = [{'id': e.id, 'label': e.nom} for e in etablissements]
        else:
            result = [{'id': e.id, 'label': '%s (%s)' % (e.nom, e.pays.nom), 'value': e.nom} 
                      for e in etablissements]
    else:
        result = None
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def etablissement_json(request, id):
    etablissement = ref.Etablissement.objects.get(id=int(id))
    result = {}
    for f in etablissement._meta.fields:
        result[f.name] = getattr(etablissement, f.attname)
    json = simplejson.dumps(result,
                            default=lambda obj: obj.isoformat if hasattr(obj, 'isoformat') else '')
    return HttpResponse(json, mimetype='application/json')
