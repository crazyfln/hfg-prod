from .base import *
import urlparse
import dj_database_url

DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

DEBUG= False


CONTACT_EMAIL = 'info@homeforgrandma.com'

redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
        },
    },
}


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = "/home/dotcloud/data/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)

#SECRET_KEY =  os.environ.get('DJANGO_SECRET_KEY','boo')
SECRET_KEY = get_env_setting('SECRET_KEY')

#TODO:
#set secret key as env variable??
#media root??
#cache settings??

DEFAULT_FILE_STORAGE = 'app.storage.S3PipelineStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_QUERYSTRING_AUTH = False
AWS_QUERYSTRING_EXPIRE = False

MEDIA_URL = "https://s3-us-west-2.amazonaws.com/hfg/"

#put the cloudfront distro here
#AWS_S3_CUSTOM_DOMAIN = "foo.cloudfront.net"


#s3
#MEDIA_URL = "https://s3-us-west-2.amazonaws.com/patronagestatic/"

#cloudfront
MEDIA_URL = ""

EMAIL_BACKEND = 'django_mandrill.mail.backends.mandrillbackend.EmailBackend'
MANDRILL_API_KEY = get_env_setting('MANDRILL_APIKEY')

STRIPE_PUBLIC_KEY = get_env_setting('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = get_env_setting('STRIPE_SECRET_KEY')

AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')

GOOGLE_MAPS_API_KEY = 'AIzaSyBkALfG9TkfOTDoWdEKqSfWid12Q2uOrhk'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(environ.get('GEOS_LIBRARY_PATH'))
GDAL_LIBRARY_PATH = "{}/libgdal.so".format(environ.get('GDAL_LIBRARY_PATH'))
