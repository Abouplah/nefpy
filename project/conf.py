DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'rigl',
        'USER': 'rigl',
        'PASSWORD': 'bonjour',
        'HOST' : 'localhost',
        'PORT' : '',
    }
}

# Don't share this with anybody.
SECRET_KEY = ''

ENV = 'TEST'

RIGL_URL = ""
SEP_URL = ""

SEP_URLS = {
    'DEV':'http://127.0.0.1:8080/api/chercheurs/',
    'TEST':'http://test.savoirsenpartage.auf.org/api/chercheurs/',
    'PROD':'http://www.savoirsenpartage.auf.org/api/chercheurs',
    }