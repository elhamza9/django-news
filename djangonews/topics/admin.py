from django.contrib import admin
from .models import Topic

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)