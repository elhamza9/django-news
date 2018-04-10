from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class Topic(models.Model):
    published_at = models.DateTimeField(blank=False, null=False)
    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.CharField(blank=False, null=False, max_length=100)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author of the Topic')
    
    class Meta:
        db_table = 'topics'
        ordering = ['published_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    published_at = models.DateTimeField(blank=False, null=False, default=timezone.now())
    content = models.TextField(blank=False, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments', verbose_name='related Topic')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author of the comment')

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.content[:10]