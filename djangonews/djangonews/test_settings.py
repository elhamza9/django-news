from .settings import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver', os.environ.get('USED_DOMAIN')]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}