# -*- encoding: utf-8 -*-

import os
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS
from conf import *

PROJET_TITRE = u"RIGL"

# Rapports d'erreurs
EMAIL_SUBJECT_PREFIX = '[rigl - %s] ' % socket.gethostname()
ADMINS = ()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

gettext = lambda s: s
CMS_LANGUAGES = (
    ('fr', gettext('French')),
    )

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'auf.django.skin',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'raven.contrib.django',
    'auf.django.references',
    'pagination',
    'chercheurs',
    'ajax_select',
    'rigl',

    # Django CMS
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    # Django plugins
    'tinymce',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.picture',

    # Recherche
    'haystack',
    'recherche',
)

MIDDLEWARE_CLASSES = (
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auf.django.piwik.middleware.TrackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',

    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',

    'auf.django.skin.context_processors.auf',
    'project.context_processors.rigl_url',
    'project.context_processors.sep_url',

)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__), "templates/rigl"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

PAYS_SOUS_REGION =  (
    'BI', # Burundi
    'CD', # Republique democratique du Congo
    #'UG', # Uganda
    'RW', # Rwanda
    #'MW', # Malawi
    #'ZM', # Zambie
    #'MZ', # Mozambique
    #'TZ', # Tanzanie
    #'KE', #Kenya    
)

AJAX_LOOKUP_CHANNELS = {
    'etablissements'  : ('chercheurs.catalogue', 'EtablissementLookup')
    }

# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'staticfiles'

CMS_TEMPLATES = (
    #('template_menu_horizontal.html', "Template du horizontal"),
    ('template_menu_vertical.html', "Template menus"),
)

# Restriction des plugins au niveau des placeholder
CMS_PLACEHOLDER_CONF = {
    #'template_menu_horizontal.html titre_page': {
    #    "plugins": ['TextPlugin']
    #},
    #
    'template_menu_vertical.html titre_page': {
        "plugins": ['TextPlugin']
    },
    'image': {
        'plugins': ['PicturePlugin'],
        'name':gettext("Image"),
    },
}

HAYSTACK_SITECONF = 'recherche.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(SITE_ROOT, 'whoosh')

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins' : 'table,paste',
    'theme_advanced_buttons1' :
    "formatselect,styleselect,|,bold,italic,underline,|,bullist,numlist,outdent,indent,|,undo,redo,|,link,unlink,image,|,backcolor,",
    'theme_advanced_buttons2' : "tablecontrols,|,removeformat,visualaid,code",
    'theme_advanced_buttons3' : "",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_toolbar_align' : "left",
    'width' : "800",
    'height' : "200",
    'theme_advanced_resizing' : "true",
    'custom_undo_redo_levels': 10,
    'theme_advanced_toolbar_location' : 'top',
    'style_formats' : (
								{'title' : 'Citation', 'selector' : 'p', 'classes' : 'citation'},
                {'title' : 'Boîte info', 'inline' : 'div', 'classes' : 'box_info'},
                {'title' : 'Boîte afficher/cacher', 'inline' : 'div', 'classes' : 'box_collapsible'},
                {'title' : 'Lien interne', 'selector': 'a', 'classes' : 'internal-link'},
                {'title' : 'Lien externe', 'selector': 'a', 'classes' : 'external-link'},
                {'title' : 'Lien id.auf', 'selector': 'a', 'classes' : 'idauf-link'},
                {'title' : 'Lien Acces Restreint', 'selector': 'a', 'classes' : 'restricted-link'},
                {'title' : 'Lien Telechargement', 'selector': 'a', 'classes' : 'download-link'},
								{'title' : 'Notes', 'inline' : 'span', 'classes' : 'notes'},
        ),

}
