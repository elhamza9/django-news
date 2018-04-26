
import pytest

from model_mommy import mommy

from topics.models import Topic, Comment, Upvote

from topics.forms import TopicForm, CommentForm, UpvoteForm

def get_random_text():
    return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam metus mi, facilisis vel vulputate eu, gravida nec purus. Nullam pulvinar congue ligula, eget porta sapien sagittis ut. In aliquet, mi a feugiat imperdiet, purus nibh laoreet lectus, placerat convallis neque est rutrum nunc. Praesent nec tellus vel nisl auctor accumsan. Vivamus dolor enim, sodales efficitur blandit ac, ullamcorper a ligula. Fusce suscipit commodo massa non malesuada. In a augue et odio placerat aliquet. Praesent iaculis a nulla eu suscipit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam vel bibendum magna. Donec ut massa et metus finibus posuere. Cras tempus cursus tortor. Cras mattis, justo sit amet ornare venenatis, libero metus pretium arcu, non fringilla augue metus id arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;'


def test_comment_form_valid():
    '''
        Tests that the CommentForm validates valid input
    '''
    form = CommentForm( data={'content' : get_random_text()} )
    assert form.is_valid() == True


def test_comment_form_invalid():
    '''
        Tests that the CommentForm doesn't validate invalid input
    '''
    form = CommentForm( data={'content' : ''} )
    assert form.is_valid() == False


@pytest.mark.django_db
def test_topic_form_valid():
    '''
        Tests that the TopicForm validates valid input
    '''
    form = TopicForm( data={'title': 'some normal title', 'slug': 'nome-normal-topic',  'content' : get_random_text()} )
    assert form.is_valid() == True

@pytest.mark.django_db
def test_topic_form_invalid():
    '''
        Tests that the TopicForm doesn't validate invalid input
    '''
    # No title
    form = TopicForm( data={'title': '', 'slug': 'nome-normal-topic',  'content' : get_random_text()} )
    assert form.is_valid() == False
    # No slug
    form = TopicForm( data={'title': 'some normal title', 'slug': '',  'content' : get_random_text()} )
    assert form.is_valid() == False
    # No content
    form = TopicForm( data={'title': '', 'slug': 'nome-normal-topic',  'content' : ''} )
    assert form.is_valid() == False

@pytest.mark.django_db
def test_upvote_form_valid():
    '''
        Tests that the UpvoteForm works
    '''
    upvote = mommy.make('topics.Upvote')
    form = UpvoteForm(instance=upvote, data={})
    assert form.is_valid() == True