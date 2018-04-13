from django.contrib import admin
from .models import Topic, Comment

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'content', 'author', 'published_at')
    class Meta:
        model = Topic
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Topic, TopicAdmin)