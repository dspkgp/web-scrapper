from celery import Celery

app = Celery('indeed', broker="amqp://guest@rabbitmq", include=['tasks'])


MONGO_SETTINGS = {
    'DB_NAME' : 'indeed',
    'HOST' : 'db',
    'PORT' : 27017,
    'USERNAME' : '',
    'PASSWORD' : ''
}

ELASTICSEARCH_SETTINGS = {
    'address' : 'http://search:9200'
}

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers' : {
        'default' : {
            'level':'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'encoding': 'utf-8',
            'filename': 'title.log'
        }
    },
    'loggers' :  {
        'indeed' : {
            'handlers' : ['default'],
            'level' : 'DEBUG',
            'propogate' : True,
        }
    }
}
