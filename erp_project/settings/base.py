import os
from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'core',
    'common',
    'inventory',
    'financial',
    'reports',
    'laundry',
    'restaurant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.auth.AuthenticationMiddleware',
    'common.middleware.database_middleware.DynamicDatabaseMiddleware',
]

ROOT_URLCONF = 'erp_project.urls'
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'common' / 'templates',
        ],
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

WSGI_APPLICATION = 'erp_project.wsgi.application'

# ============================================================================
# DATABASE CONFIGURATION - HYBRID APPROACH
# ============================================================================
"""
Database Strategy:

1. MAIN Database ('default'):
   - Django sessions (django_session)
   - Django auth (User, Group, Permission)
   - Django admin, contenttypes, messages
   - Authentication tables (itemgroups, customers, softwares)
   - Credentials from .env file

2. Customer Database ('customer_db'):
   - All customer-specific data
   - common app models (Organization, CompanyInformation)
   - laundry app models
   - restaurant app models
   - inventory app models
   - financial app models
   - Dynamically configured per user from softwares table
"""

try:
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    env_path = BASE_DIR / '.env'
    load_dotenv(env_path)
    
    # Get MAIN database credentials from .env
    db_host = os.getenv('DB_HOST', '')
    db_port = os.getenv('PORT', '5432')
    db_name = os.getenv('DB_NAME', '')
    db_user = os.getenv('DB_USER', '')
    db_password = os.getenv('DB_PASSWORD', '')
    
    # Configure MAIN database
    if db_host and db_name and db_user:
        # PostgreSQL MAIN database
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {
                    'connect_timeout': 10,
                },
            }
        }
        print(f"✓ Configured MAIN database: {db_host}/{db_name}")
    else:
        # Fallback to SQLite if credentials not configured
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'main.db',
            }
        }
        print("⚠ Using SQLite fallback for MAIN database")
        
except Exception as e:
    # Fallback to SQLite on any error
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'main.db',
        }
    }
    print(f"⚠ Database configuration error: {e}")
    print("⚠ Using SQLite fallback")

# CUSTOMER DATABASE - Customer-specific data
# This will be dynamically configured by the middleware based on session data
# Customer database credentials come from the 'softwares' table in MAIN database
DATABASES['customer_db'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'placeholder',  # Will be replaced by middleware
    'USER': 'placeholder',
    'PASSWORD': 'placeholder',
    'HOST': 'placeholder',
    'PORT': '5432',
    'ATOMIC_REQUESTS': False,
    'AUTOCOMMIT': True,
    'CONN_MAX_AGE': 0,  # Don't persist connections (credentials change per user)
    'OPTIONS': {
        'connect_timeout': 10,
    },
}

# ============================================================================
# DATABASE ROUTER
# ============================================================================
DATABASE_ROUTERS = ['common.db_router.CustomerDatabaseRouter']

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
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'common' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
(BASE_DIR / 'logs').mkdir(exist_ok=True)