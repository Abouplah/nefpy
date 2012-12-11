# -*- encoding: utf-8 -*-

try:
    from auf.django.references import models as ref
except:
    ref = None

from django.conf import settings

PROJET_TITRE_KEY = 'PROJET_TITRE'

def auf(request):
    """
    """
    # Nom du projet
    site = getattr(settings, PROJET_TITRE_KEY, None)
    if not site:
        site = "Créer une clef '%s' dans settings.py" % PROJET_TITRE_KEY

    # le User peut changer de mdp s'il est local
    if ref is not None:
        try:
            email = request.user.email
            can_change_password = not ref.Authentification.objects.filter(courriel=email).exists() 
        except:
            can_change_password = None
    else:
        can_change_password = True
    return {
        'AUF_SITE' : site,
        'can_change_password' : can_change_password,
    }
