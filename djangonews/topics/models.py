from django.db import models

# Create your models here.

class Topic(models.Model):
    published_at = models.DateTimeField(blank=False, null=False)
    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.CharField(blank=False, null=False, max_length=100)
    content = models.TextField(blank=False, null=False)
    
    class Meta:
        db_table = 'topics'
        ordering = ['published_at']

    def __str__(self):
        return self.title