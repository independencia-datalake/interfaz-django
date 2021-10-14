from pathlib import Path, os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ipqwifh56s24&(umy3!m)w#j3$i57)r=ycjdh7d1#jrero&s!#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['sistema.independenciaciudadana.cl','www.sistema.independenciaciudadana.cl', '54.94.42.27']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Personales
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'farmacia.apps.FarmaciaConfig',
    'formulario.apps.FormularioConfig',
    'calculadorauv.apps.CalculadorauvConfig',
    'vis.apps.VisConfig',
    'dimap.apps.DimapConfig',
    'seguridad.apps.SeguridadConfig',
    
    # De terceros
    'crispy_forms',
    'django_filters',
    'storages',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datalake.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'datalake.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'datalake_db',
   }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'datalake_master',
#         'PASSWORD': 'D4t4l4k3db.',
#         'HOST': 'datalake-db.cplck86bddfa.sa-east-1.rds.amazonaws.com',
#         'PORT': 5432
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Chile/Continental'
#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'core-home'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#CONFIGURACION DEL S3 AWS
AWS_ACCESS_KEY_ID = "AKIARUEETZAVW7RERMGW"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "independenciabucket"

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_LOCATION = 'media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

