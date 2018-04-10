from django.apps import AppConfig


class TopicsConfig(AppConfig):
    name = 'topics'
    def ready(self):
        import topics.signals