from django.forms import ModelForm

from .models import Comment, Upvote

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('published_at', 'author', 'topic')

class UpvoteForm(ModelForm):
    class Meta:
        model = Upvote
        exclude = ('timestamp', 'upvoter', 'topic')