from .settings import *
import os

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
# CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enables whitenoise for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.PinCodeMiddleware',
    'main.middleware.NotFoundMiddleware'
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEBUG = False

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("aitu-websocket.redis.cache.windows.net", 6380)],
#             "password": "mDsSBp6CO41WoPtDeIzU3drvaDbO4gcyRAzCaJfmfDc=",
#             "ssl_cert_reqs": None,
#             "ssl_ca_certs": None,
#         },
#     },
# }