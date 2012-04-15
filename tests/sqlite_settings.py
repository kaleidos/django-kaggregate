DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = "django_tests_secret_key"

#LOGGING = { 
#    'version': 1,
#    'disable_existing_loggers': True,
#    'formatters': {
#        'standar': {
#            'format': '%(asctime)s: %(message)s',
#        },  
#    },  
#    'handlers': {
#        'null': {
#            'level':'DEBUG',
#            'class':'django.utils.log.NullHandler',
#        },  
#        'console':{
#            'level':'DEBUG',
#            'class':'logging.StreamHandler',
#            'formatter': 'standar'
#        }
#    },
#    'loggers': {
#        'django.db.backends':{
#            'handlers': ['console'],
#            'level': 'DEBUG',
#            'propagate': False,
#        },
#    }
#}
