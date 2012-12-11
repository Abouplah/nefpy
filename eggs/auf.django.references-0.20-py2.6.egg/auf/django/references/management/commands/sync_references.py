# encoding: utf-8

from django.core.management.base import BaseCommand
from django.db.models import get_models

from auf.django.references import models as ref

class Command(BaseCommand):
    help = 'Synchronise les données de références AUF'

    def handle(self, *args, **options):
        for model in get_models():
            if issubclass(model, ref.EtablissementBase):
                self.stdout.write('Mise à jour de %s.%s...\n' %
                                  (model._meta.app_label, model.__name__))
                for obj in model._default_manager.exclude(ref=None):
                    for f in obj.ref._meta.fields:
                        if f.name != 'id':
                            setattr(obj, f.attname, getattr(obj.ref, f.attname))
                    obj.save()
