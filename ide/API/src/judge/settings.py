"""
Django settings for judge project.
"""

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'epm0px=%*4yw0&_bc8=@htr3yu$e)!y&lu@g7u_5%gw0^3kxgo'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow host at any IP and port (as only port 8000 is opened in Docker)
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sslserver',
    'corsheaders',
    'submission',
    'logger'    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',    # CSRF disabled temporarily
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.logger.RequestLogMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

# Root URL config file
ROOT_URLCONF = 'judge.urls'


# Templates for frontend (Admin panel only)
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


WSGI_APPLICATION = 'judge.wsgi.application'


# Database

DATABASES = {
    # PostgreSQL
    # Get parameters/credentials from environment variables
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'submissions'),
        'USER': os.environ.get('DB_USER', 'djangoconn'),
        'PASSWORD': os.environ.get('DB_PWD', 'django_1234'),
        'HOST': os.environ.get('DB_HOST', '172.17.0.2'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
    'logger': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'logger'),
        'USER': os.environ.get('DB_USER', 'djangoconn'),
        'PASSWORD': os.environ.get('DB_PWD', 'django_1234'),
        'HOST': os.environ.get('DB_HOST', '172.17.0.2'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

DATABASE_ROUTERS = ['logger.router.LogRouter']

# LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logger.handlers.DBHandler',
            'model': 'logger.models.GeneralLog',
            'expiry': 86400,
            'formatter': 'verbose'
        },
        'db': {
            'level': 'INFO',
            'class': 'logger.handlers.DBHandler',
            'model': 'logger.models.SpecialLog',
            'expiry': 86400,
        },
    },
    'loggers': {
        'customLog': {
            'level': 'INFO',
            'handlers': ['db'],
            'propagate': True,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['default'],
            'propagate': True,
        },
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
