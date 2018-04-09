from django.contrib import admin

from . import models

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Topic, TopicAdmin)