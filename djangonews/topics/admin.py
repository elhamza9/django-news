from django.contrib import admin
from .models import Topic, Comment

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)