import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
channel_layer = channels.asgi.get_channel_layer()

# class InvalidChannelLayerError(ValueError):
    # pass

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6378')],
        },
        "ROUTING": "chat.routing.channel_routing",
    },
}


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
