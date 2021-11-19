# -*- coding: utf-8 -*-
# Django settings for paquetin project.
import os
from django.conf.global_settings import DATETIME_INPUT_FORMATS

PROJECT_PATH    = os.path.realpath(os.path.dirname(__file__))
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
SITE  = 1

URL_EXTERN_APP_ZOPE     = "http://zope:8081/gestform.com/planning/of_ordre_fabrication_v2.00/of_conditionnement/gestion_ordre_fabrication/"
URL_EXTERN_APP_ATHENA   = "http://athena:8084/gestform.dev/commande_client/charge_condt/plan_charge/of_ordre_fabrication_v2.00/of_conditionnement/"



DATETIME_INPUT_FORMATS += ('%Y-%m-%d %I:%M %p', '%Y-%m-%d %H:%M')


project_name = 'planning of Pulsar.Sce'
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'planning.db'),
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}


DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.mysql', #
        'NAME': 'ofschedule',
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'grutil001',
        'HOST': 'localhost',         # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                  # Set to empty string for default.
    }
}

"""

DATABASES = {
    # avce ODBC django-pyodbc-azure-1.11.13.1

   'default': {
       'NAME': 'GestformBDD',
       ## 'ENGINE': 'django.db.backends.sqlserver_ado',
       'ENGINE': 'sql_server.pyodbc',
       ###'HOST': "ganesh", # base pord !!
       'HOST': "athena",
       "PORT" : 1433,
       'USER': "sa",
       'PASSWORD': "Mc78Bd!%",
       'AUTOCOMMIT': True,


       'OPTIONS': {
            'host_is_server': True,
            'driver': 'ODBC Driver 17 for SQL Server',
            #'driver': 'ODBC Driver 13 for SQL Server',
            #'dsn': 'self_mssql',
            #'driver': 'SQL Server Native Client 11.0',
       },
   }
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.11.151', '192.168.10.232', '10.69.129.79', '*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'Fr-fr'

DEFAULT_CHARSET='UTF-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
# Lorsque USE_TZ vaut True et que la base de données ne gère pas les fuseaux horaires (par ex. SQLite, MySQL, Oracle), Django lit et écrit les dates/heures en heure locale en fonction de cette option quand elle est définie et en UTC si elle ne l’est pas.

USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"./manage.py bower install
MEDIA_ROOT = BASE_DIR  + '/projects/static/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = os.path.join("/var/www/django/gterpsce",   'static')

STATIC_ROOT = os.path.join(BASE_DIR,   'ofschedule', 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_PATH, 'ofschedule', 'static'),
    os.path.join(PROJECT_PATH, 'approvisionnement', 'static'),
    os.path.join(PROJECT_PATH, 'projects', 'static'),
    os.path.join(PROJECT_PATH, 'ofsce', 'static'),
    os.path.join(PROJECT_PATH, 'businessce', 'static'),
    os.path.join(PROJECT_PATH, 'static', 'vuejs'),
    os.path.join(PROJECT_PATH, 'bower_components'),
    os.path.join(PROJECT_PATH, 'media'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1-%gfd@@8lBismiALLAHE_1qfj@ix#!xig(_2zq&b&2'

# List of callables that know how to import templates from various sources.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Cache en memoire RAM

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.sock',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}
"""

ROOT_URLCONF = 'planning.urls'

# Python dotted path to the WSGI application used by Django's runserver.
# WSGI_APPLICATION = 'planning.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'debug_toolbar',
    'djangobower',
    # Authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # DRF
    'rest_framework',
    'schedule',
    # moduu=le planning
    'ofschedule',
    # module approvisionnement
    'approvisionnement',
    # module of
    'of_module',
    # BI business data Sce
    'businessce',
    # taxonomie methode de classification de l'information (search , categories, tags)
    'core.profile',
    'core.taxonomy',
    'core.widgets',
    'core.notifications',
    # 'notifications',
    #'core.calendar',
    # avatar
    'avatar',
    # todo
    'todo',
    # gestion de projet
    'projects',
    #taggit
    'taggit',
    # django notifications x (django-notify-x)
    'notify',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_CONFIG = None # Désactivation de la configuration de journalisation
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'formatters': {
        'console': {
            # création d'un formateur qui va ajouter le temps, le niveau
            # de chaque message quand on écrira un message dans le log
            'format': '%(levelname)-8s %(message)s',
        },
        'file': {
            # création d'un formateur qui va ajouter le temps, le niveau
            # de chaque message quand on écrira un message dans le log
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG', # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },

        'planning': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            # required to avoid double logging with root logger
            'propagate': False,
        },
        # on  lui dit qu'il doit afficher les log de mon modules 'ofschedule'
        'ofschedule': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },

}

BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap',
    'moment',
    'fullcalendar',
    'bootstrap_table',
    'pandas_bootstrap_table'
)

TEMPLATES = [
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
         os.path.join(BASE_DIR,  'ofschedule', 'templates', 'of'),
         os.path.join(BASE_DIR,  'approvisionnement', 'templates', 'da'),
         os.path.join(BASE_DIR,  'businessce', 'templates', 'console'),
         os.path.join(BASE_DIR,  'of_module', 'templates', 'of' ),
         os.path.join(BASE_DIR, 'ofschedule', 'templates', 'allauth'),
         os.path.join(BASE_DIR, 'ofschedule', 'templates', 'admin'),
         os.path.join(BASE_DIR,  'ofschedule', 'templatetags'),
         os.path.join(BASE_DIR,  'approvisionnement', 'templates', 'da'),
         os.path.join(BASE_DIR,  'projects', 'templates'),
         os.path.join(BASE_DIR,  'projects', 'templates', 'projects' ),
         os.path.join(BASE_DIR,  'projects', 'templates', 'notifications' ),
         os.path.join(BASE_DIR,  'projects', 'templates', 'notifications',  'includes'),
         os.path.join(BASE_DIR,  'projects', 'templates', 'widgets'),
         os.path.join(BASE_DIR,  'core', 'templatetags'),
             ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
             # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages'
        ],

        'libraries':{
            'breadcrumbs': 'core.templatetags.breadcrumbs',
            'details': 'core.templatetags.details',
            #'region': 'core.templatetags.region',

            }
    },
}]

# allauth params
"""
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = 'none'
LOGIN_REDIRECT_URL = 'of/home/'
"""

##################
# AUTHENTICATION #
##################
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_AUTHENTICATION_METHOD = 'username'

AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/accounts/login/'

# The number of days a password reset link is valid for
PASSWORD_RESET_TIMEOUT_DAYS = 3


AUTH_PASSWORD_VALIDATORS = []
###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}

# Default exception reporter filter class used in case none has been
# specifically assigned to the HttpRequest instance.
DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'


# -------------------------------------
# projects
# -------------------------------------
"""
PROJECT_STATUS_CHOICES = [ ("O" , "Ouvert"), ("E", "En cours"), ("C", "Cloturé"),  ("N", "Annulé"),]
PROJECT_DEFAULT_STATUS = "Ouvert"
PROJECT_CLOSE_STATUSES  = [ (1, "Termine"),  (2, "Annulé"),]

TICKET_TYPE_CHOICES  = [("A" , "Anomalie"),  ("I", "incident"), ]
TICKET_DEFAULT_TYPE     = "Anomalie"
TICKET_URGENCY_CHOICES  = [("U", "Urgent"),  ("N", "Normal"),]
TICKET_DEFAULT_URGENCY  = "Urgent"

TICKET_DEFAULT_STATUS   = "Ouvert"
TICKET_STATUS_CHOICES   = [("O" , "Ouvert"), ("E", "En cours"), ("C", "Cloturé"),  ("N", "Annulé"),]
TICKET_CLOSE_STATUSES   = [("T" "Termine"), ("N", "Annulé"),]
"""
VISIBILITE_CHOICES = [("P" , "Projet Public"), ("I", "Projet interne"), ("C", "Projet lié à un client"),  ("V", "Projet privé seulement au abonnés"),]
VISIBILITE_DEFAULT = "Projet Public"


# import des variables taxonomy
from taxonomy import SEARCH_IN_MODELS

# import des variables projects
from projects import *

FILE_UPLOAD_MAX_MEMORY_SIZE = 20 # 2621440 (c-à-d. 2.5 Mio).


#------------------------------
# DJANGO REST  framework
#------------------------------
# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}
