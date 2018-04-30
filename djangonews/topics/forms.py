from django.forms import ModelForm, CharField

from tinymce import TinyMCE

from .models import Topic, Comment, Upvote
'''
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
'''
class TopicForm(ModelForm):
    content = CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 100, 'rows': 20}
        )
    )
    class Meta:
        model = Topic
        exclude = ('published_at', 'author', 'nbr_upvotes', 'nbr_comments')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('published_at', 'author', 'topic')

class UpvoteForm(ModelForm):
    class Meta:
        model = Upvote
        exclude = ('timestamp', 'upvoter', 'topic')