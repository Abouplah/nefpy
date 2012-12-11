# -*- coding: utf-8 -*-

from ajax_select import LookupChannel
from django.db.models import Q
from django.conf import settings
from auf.django.references import models as ref


class EtablissementLookup(LookupChannel):

    model = ref.Etablissement

    def check_auth(self, request):
        return True

    def get_query(self, q, request):
        q_rigl = Q(pays__code__in=settings.PAYS_SOUS_REGION)
        etablissements = ref.Etablissement.objects.filter(q_rigl)
        return etablissements.filter(
                Q(nom__icontains=q) |
                Q(pays__nom__istartswith=q) |
                Q(pays__code__istartswith=q)).order_by('nom')

    def get_result(self, obj):
        return obj.nom

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return u"[%s] %s" % (obj.pays.nom, obj.nom)
