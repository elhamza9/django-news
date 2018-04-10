from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Topic, Upvote
import os.path

@receiver(post_save, sender=Upvote)
def upvote_post_save(sender, instance, **kwargs):
    print('Upvote was saved, let increment count {}'.format(instance))
    upvoted_topic = instance.topic
    upvoted_topic.nbr_upvotes += 1
    upvoted_topic.save()