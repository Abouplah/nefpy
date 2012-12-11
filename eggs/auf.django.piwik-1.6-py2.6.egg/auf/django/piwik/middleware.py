# -*- coding: utf-8 -*-

import re

from django.conf import settings

try:
    import auf.django.references.models as ref
    REFERENCES_CHARGEES = True
except:
    REFERENCES_CHARGEES = False
    

from settings import PIWIK_TOKEN, PIWIK_HOST, PIWIK_HTTPFORCE,\
    PIWIK_TRACKCODE, PIWIK_EXCLUDE_REFERER


ire_body = re.compile(re.escape('</body>'), re.IGNORECASE)


class TrackMiddleware:

    def process_response(self, request, response):
        """
        Trackcode injection avant le body s'il y a un token piwik dans la conf
        locale.
        """
        if PIWIK_TOKEN is None:
            return response

        http_referer = request.META.get('HTTP_REFERER', "")
        referer = http_referer
        
        for excl in PIWIK_EXCLUDE_REFERER:
            if excl in http_referer:
                referer = ""
                break

        if request.is_secure() and not PIWIK_HTTPFORCE:
            protocol = "https"
        else:
            protocol = "http"

        user = getattr(request, 'user', None)
        if user and REFERENCES_CHARGEES and user.is_authenticated():
            try:
                employe = ref.Employe.objects.get(courriel=request.user.email)
                imp_id = employe.implantation.id
                implantation = "piwikTracker.setCustomVariable(1, 'implantation', '%s', 'visit');" % imp_id
            except :
                pass
        else:
            implantation = ""

        track = PIWIK_TRACKCODE % {
                'host': PIWIK_HOST,
                'token': PIWIK_TOKEN,
                'protocol': protocol,
                'static': settings.STATIC_URL,
                'referer': referer,
                'implantation': implantation,
                }
        content = response.content
        content_with_trackcode = ire_body.sub('%s</body>' % track, content)
        response.content = content_with_trackcode
        return response
