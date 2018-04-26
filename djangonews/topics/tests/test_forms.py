
import pytest

from model_mommy import mommy

from topics.models import Topic, Comment, Upvote

from topics.forms import TopicForm, CommentForm

def get_random_text():
    return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam metus mi, facilisis vel vulputate eu, gravida nec purus. Nullam pulvinar congue ligula, eget porta sapien sagittis ut. In aliquet, mi a feugiat imperdiet, purus nibh laoreet lectus, placerat convallis neque est rutrum nunc. Praesent nec tellus vel nisl auctor accumsan. Vivamus dolor enim, sodales efficitur blandit ac, ullamcorper a ligula. Fusce suscipit commodo massa non malesuada. In a augue et odio placerat aliquet. Praesent iaculis a nulla eu suscipit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam vel bibendum magna. Donec ut massa et metus finibus posuere. Cras tempus cursus tortor. Cras mattis, justo sit amet ornare venenatis, libero metus pretium arcu, non fringilla augue metus id arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;'


def test_comment_form_valid():
    '''
        Tests that the form validates valid input
    '''
    form = CommentForm( data={'content' : get_random_text()} )
    assert form.is_valid() == True


def test_comment_form_invalid():
    '''
        Tests that the form doesn't validate valid input
    '''
    form = CommentForm( data={'content' : ''} )
    assert form.is_valid() == False