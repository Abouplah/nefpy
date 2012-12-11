# -*- encoding: utf-8 -*-

from conf import RIGL_URL, SEP_URL

# Ajout de variables accessibles dans les templates (pour tester permissions dans templates)

def rigl_url(request):
    return {'RIGL_URL': RIGL_URL}

def sep_url(request):
    return {'SEP_URL': SEP_URL}

