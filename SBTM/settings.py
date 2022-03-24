#-*-coding:utf-8 -*-，
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2*o3ecg5%aevlq+dl*#*vm3*-&tezwzf-b)1sz#f6y=gb(t)bb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'reversion',
    'charts.apps.ChartsConfig',
    'users.apps.UsersConfig',
    'course.apps.CourseConfig',
    'operation.apps.OperationConfig',
    'organization.apps.OrganizationConfig',
    'captcha',
    'pure_pagination',
    'DjangoUeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.LoggingMiddleware.LogMiddle'
]

ROOT_URLCONF = 'SBTM.urls'
AUTH_USER_MODEL = 'users.UserProfile'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
	    ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'SBTM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    },
    # 'db': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': str(BASE_DIR / 'db2.sqlite3'),
    # }
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# 发送邮箱
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 456
EMAIL_HOST_USER = "631230485@qq.com"
EMAIL_HOST_PASSWORD = "fulihua09263319"
EMAIL_USE_TLS= True
# EMAIL_USE_SSL = True
EMAIL_FROM = "631230485@qq.com"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# DATABASE_ROUTERS = ['db_router.MasterSlaveDBRouter']
# DATABASE_APPS_MAPPING = {
#     # 'users': 'default',
#     'charts': 'db',
#     'course': 'db',
#     'operation': 'db',
#     'organization': 'db',
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR,'static')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOG_PATH = os.path.join(BASE_DIR,'LOG')

# 官网：https://docs.djangoproject.com
# 中文loggin配置：https://docs.djangoproject.com/zh-hans/2.2/topics/logging/

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             # 'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
#             'format': '%(asctime)s %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename':  '%s/%s' % (LOG_PATH, 'asmBAK.log'),
#             'formatter': ''
#         },
#         'file': {
#             # 实际开发建议使用WARNING
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             # 日志位置,日志文件名,日志保存目录必须手动创建，然后给对应的路径即可 注：这里的文件路径要注意BASE_DIR
#             'filename':  '%s/%s' % (LOG_PATH, 'asm.log'),
#             # 日志文件的最大值,这里我们设置300M
#             'maxBytes': 300 * 1024 * 1024,
#             # 日志文件的数量,设置最大日志数量为10
#             'backupCount': 10,
#             # 日志格式:详细格式
#             'formatter': '',
#             # 设置日志中的编码
#             'encoding': 'utf-8'
#         },
#     },
#     # 日志对象
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
#         },
#     }
# }


LOGGING = {
    'version': 1,
    # 禁用日志
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            # 将系统接受到的体制，交给handler去处理
            'handlers': ['default','console','info'],
            'level': 'INFO',
            # 'propagate': False,
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/%s' % (LOG_PATH, 'asm.log'),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'default',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        'console': {
            'filename': '%s/%s' % (LOG_PATH, 'asmBAK.log'),
            'level': 'ERROR',
            # 指定日志的格式
            'formatter': '',
            # 备份
            # 'filters':'require_debug_true',    # 设定过滤器
            # 'class': 'logging.StreamHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件大小：5M
            'maxBytes': 5 * 1024 * 1024,
            'encoding':"utf-8"
        },
        'info': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/%s' % (LOG_PATH, 'asminfo.log'),
            'formatter': '',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'encoding': 'utf-8',  # 设置默认编码
        },
    },

    'formatters': {
        'default': {
            'format': '%(levelname)s  %(module)s %(message)s'
        }
    }
}
