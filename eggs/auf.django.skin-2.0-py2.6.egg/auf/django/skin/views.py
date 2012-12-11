# -*- encoding: utf-8 -*-

from django.template import Context, RequestContext
from django.shortcuts import render_to_response

def demo(request,):
    """
    Page pour montrer la charte graphique de l'AUF
    """
    breadcrumb = (
        ("/" , "Accueil"),
        ("#" , "Demo charte graphique AUF"), 
    )
    c = {'breadcrumb' : breadcrumb}
    return render_to_response("skin/demo.html",
        Context(c),
        context_instance = RequestContext(request)
        )


