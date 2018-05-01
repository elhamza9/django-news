from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Topic, Upvote, Comment
import os.path

@receiver(post_save, sender=Upvote)
def upvote_post_save(sender, instance, **kwargs):
    print('Upvote was saved, let increment count {}'.format(instance))
    upvoted_topic = instance.topic
    upvoted_topic.nbr_upvotes += 1
    upvoted_topic.save()

@receiver(post_delete, sender=Upvote)
def upvote_post_delete(sender, instance, **kwargs):
    print('Upvote was deleted, lets decrement count {}'.format(instance))
    upvoted_topic = instance.topic
    upvoted_topic.nbr_upvotes -= 1
    if upvoted_topic.nbr_upvotes > -1:
        upvoted_topic.save()

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, **kwargs):
    print('Comment was saved, let increment count {}'.format(instance))
    commented_topic = instance.topic
    commented_topic.nbr_comments += 1
    commented_topic.save()

@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
    print('Comment was deleted, lets decrement count {}'.format(instance))
    commented_topic = instance.topic
    commented_topic.nbr_comments -= 1
    if commented_topic.nbr_comments > -1:
        commented_topic.save()