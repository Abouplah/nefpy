# -*- encoding: utf-8 -*- 
from django import forms

from django import forms
from django.conf import settings
from ajax_select.fields import AutoCompleteField
from auf.django.references import models as ref
from project.chercheurs.models import ChercheurSearch


class DisciplineProxy(ref.Discipline):
    def __unicode__(self):
        return self.nom

    class Meta:
        proxy = True

class EtablissementProxy(ref.Etablissement):
    def __unicode__(self):
        return self.nom

    class Meta:
        proxy = True

class ChercheurSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les chercheurs."""
    pays = forms.ModelChoiceField(queryset=ref.Pays.objects.filter(code__in=settings.PAYS_SOUS_REGION), required=False)
    discipline = forms.ModelChoiceField(queryset=DisciplineProxy.objects.all(), required=False)
    etablissement_libre = AutoCompleteField('etablissements', required=False,
            label="Établissement",
            help_text=u"Taper le nom de l'établissement ou son pays")


    def __init__(self, *args, **kwargs):
        super (ChercheurSearchForm,self ).__init__(*args,**kwargs)

    class Meta:
        model = ChercheurSearch
        exclude = ('etablissement', )

