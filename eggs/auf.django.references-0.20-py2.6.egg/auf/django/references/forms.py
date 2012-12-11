# encoding: utf-8

from django import forms
from django.utils.safestring import mark_safe

from auf.django.references import models as ref


class EtablissementAutocompleteWidget(forms.TextInput):
    """
    Champ texte qui émet les invocations javascript pour gérer
    l'autocomplétion des établissements.
    """

    def __init__(self):
        super(EtablissementAutocompleteWidget, self).__init__(attrs={
            'autocomplete': 'off'
        });
        self.exclude_refs = None

    def render(self, name, value, attrs=None):
        widget = super(EtablissementAutocompleteWidget, self).render(name, value, attrs=attrs)
        id = attrs and attrs.get('id')
        if id:
            args = ("'%s'" % self.exclude_refs) if self.exclude_refs else ''
            js = """
                 <script type="text/javascript">
                 $(function() { $('#%s').etablissement_autocomplete(%s); })
                 </script>
                 """ % (id, args)
            widget += js
        return mark_safe(widget)


class EtablissementForm(forms.ModelForm):
    nom = forms.CharField(widget=EtablissementAutocompleteWidget)

    class Meta:
        model = ref.EtablissementBase

    class Media:
        css = {
            'screen': ('references/jquery-ui.css',)
        }
        js = (
            'references/jquery.min.js',
            'references/jquery-ui.min.js',
            'references/jquery.etablissement-autocomplete.js',
        )

    def __init__(self, *args, **kwargs):
        super(EtablissementForm, self).__init__(*args, **kwargs)
        model = self._meta.model
        ref_name = model._meta.get_field('ref').rel.related_name
        self.fields['nom'].widget.exclude_refs = ref_name
