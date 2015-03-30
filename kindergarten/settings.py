#coding=utf-8
"""
Django settings for kindergarten project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '440=vs&b9*oemb@f)500wfsp+axlzmrz+a%4v^%!ly&)162yx7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#2 hour timeout
SESSION_COOKIE_AGE=60*60*2 #2 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'kindergarten',
    'kindergarten.admin',
    'kindergarten.web',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'kindergarten.urls'

WSGI_APPLICATION = 'kindergarten.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'kindergarten',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'postgres',
        'PASSWORD': 'pN4ixkUTpp72',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SITEROOT= BASE_DIR
UPLOADPATH= '/upload'
#使用云存储
USE_STORAGE = False

UEDITOR_SETTINGS={
            "config":{
               #这里放ueditor.config.js里面的配置项.......
            },
            "upload":{
               #这里放php/config.json里面的配置项.......
            },
            "images_upload": {
                "allow_type": "jpg,png", #定义允许的上传的图片类型
                "path": "upload/", #定义默认的上传路径
                "max_size": "2222kb"        #定义允许上传的图片大小，0代表不限制
            },
            "files_upload": {
                "allow_type": "zip,rar", #定义允许的上传的文件类型
                "path": "upload/",    #定义默认的上传路径
                "max_size":"2222kb"       #定义允许上传的文件大小，0代表不限制
            },
        }