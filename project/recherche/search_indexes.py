# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import string_concat, ugettext_lazy
from django.utils.html import strip_tags

from haystack import indexes, site

from cms.models.managers import PageManager
from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin

from project.rigl.models import Actualite


def page_index_factory(lang, lang_name):
    if isinstance(lang_name, basestring):
        lang_name = ugettext_lazy(lang_name)

    def get_absolute_url(self):
        # no language prefix
        return Page.get_absolute_url(self)

    class Meta:
        proxy = True
        app_label = 'cms'
        if len(settings.LANGUAGES) > 1:
            verbose_name = string_concat(
                    Page._meta.verbose_name, ' (', lang_name, ')')
            verbose_name_plural = string_concat(
                    Page._meta.verbose_name_plural, ' (', lang_name, ')')
        else:
            verbose_name = Page._meta.verbose_name
            verbose_name_plural = Page._meta.verbose_name_plural

    attrs = {'__module__': Page.__module__,
             'Meta': Meta,
             'objects': PageManager(),
             'get_absolute_url': get_absolute_url}

    _PageProxy = type("Page_%s" % lang.title(), (Page,), attrs)

    _PageProxy._meta.parent_attr = 'parent'
    _PageProxy._meta.left_attr = 'lft'
    _PageProxy._meta.right_attr = 'rght'
    _PageProxy._meta.tree_id_attr = 'tree_id'

    class _PageIndex(indexes.SearchIndex):
        language = lang

        text = indexes.CharField(document=True, use_template=False)
        pub_date = indexes.DateTimeField(model_attr='publication_date')
        login_required = indexes.BooleanField(model_attr='login_required')
        url = indexes.CharField(
                stored=True, indexed=False, model_attr='get_absolute_url')
        title = indexes.CharField(
                stored=True, indexed=True, model_attr='get_title')

        def prepare(self, obj):
            self.prepared_data = super(_PageIndex, self).prepare(obj)
            plugins = CMSPlugin.objects.filter(
                    language=lang, placeholder__in=obj.placeholders.all())
            text = obj.get_title()
            for plugin in plugins:
                instance, _ = plugin.get_plugin_instance()
                if hasattr(instance, 'search_fields'):
                    # so text is readable and words have spaces between
                    text += '\n'.join(strip_tags(
                        getattr(instance, field, '').replace('>', '> '))
                        for field in instance.search_fields)
                if getattr(instance, 'search_fulltext', False):
                    text += strip_tags(
                            instance.render_plugin().replace('>', '> '))
            self.prepared_data['text'] = text
            return self.prepared_data

        def index_queryset(self):
            qs = _PageProxy.objects.published()\
                    .filter(title_set__language=lang).distinct()
            return qs

    return _PageProxy, _PageIndex

for lang_tuple in settings.LANGUAGES:
    lang, lang_name = lang_tuple
    site.register(*page_index_factory(lang, lang_name))


class ActualiteIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=False)
    url = indexes.CharField(stored=True, indexed=False,
            model_attr='get_absolute_url')
    date_saisie = indexes.DateTimeField(model_attr='date_saisie')

    def get_model(self):
        return Actualite

    def prepare(self, obj):
        self.prepared_data = super(ActualiteIndex, self).prepare(obj)
        text = obj.titre
        text += obj.contenue
        self.prepared_data['text'] = text
        return self.prepared_data

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)

site.register(Actualite, ActualiteIndex)
