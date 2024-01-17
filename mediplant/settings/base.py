from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'django-insecure-66m-$ghl%c523szciay*#l3a6vy(q^m8yh$oids82ikcriig95'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'ckeditor',
    'ckeditor_uploader',
    'jdatetime',
    'encyclopedia.apps.EncyclopediaConfig',
    'city.apps.CityConfig',
    'account.apps.AccountConfig',
    'chat.apps.ChatConfig',
    'doctor.apps.DoctorConfig',
    'report.apps.ReportConfig',
    'shop.apps.ShopConfig',
    'sickness.apps.SicknessConfig',
    'web.apps.WebConfig',
    'doctor_visit.apps.DoctorVisitConfig',
    'transaction.apps.TransactionConfig',
    'sale.apps.SaleConfig',
    'product.apps.ProductConfig',
    'account_logger.apps.AccountLoggerConfig',
    'feedback.apps.FeedbackConfig',
    'banner.apps.BannerConfig',
    'django.contrib.humanize',
    'rest_framework',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mediplant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mediplant.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'account.User'
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CKEDITOR_UPLOAD_PATH = "ckeditor_media"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 960,
        'skin': 'moono-lisa',
        'uiColor': '#b7d6ec',
    },
}

CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_IMAGE_BACKEND = None
CKEDITOR_ALLOW_NONIMAGE_FILES = True
