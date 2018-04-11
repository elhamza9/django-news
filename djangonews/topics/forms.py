from django.forms import ModelForm

from .models import Topic, Comment, Upvote

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude = ('published_at', 'author', 'nbr_upvotes')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('published_at', 'author', 'topic')

class UpvoteForm(ModelForm):
    class Meta:
        model = Upvote
        exclude = ('timestamp', 'upvoter', 'topic')