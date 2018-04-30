import pytest

from django.utils import timezone
from django.db import IntegrityError

from topics.models import Topic, Comment, Upvote

from model_mommy import mommy

from datetime import datetime

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="session", autouse=True)
def setup_mommy_topic_content_html_gen():
    def mommy_html_gen():
        return '<h3>This is mommy generated content !</h3>'
    mommy.generators.add('tinymce.models.HTMLField', mommy_html_gen)

@pytest.fixture
def topic_fixture():
    "Provides a single Topic object"
    return mommy.make('topics.Topic')

@pytest.fixture
def comment_fixture():
    "Provides a single Comment object"
    return mommy.make('topics.Comment')

'''
    Test Topic Model Behaviour
'''
class TestTopic:

    def test_str(self, topic_fixture):
        '''
            Test the string representation
        '''
        assert str(topic_fixture) == topic_fixture.title, 'Topic str representation should be its title'


    def test_nbr_upvotes_comments_is_zero(self, topic_fixture):
        '''
            Test default number of upvotes / comments is zero
        '''
        assert topic_fixture.nbr_upvotes == 0,  'Initial nbr of upvotes should be zero'
        assert topic_fixture.nbr_comments == 0, 'Initial nbr of comments should be zero'


    def test_duplicate_slug(self, topic_fixture):
        '''
            Test that Exception is raised if trying
            to add a Topic with duplicate slug
        '''
        with pytest.raises(IntegrityError):
            t2 = mommy.make('topics.Topic', slug=topic_fixture.slug)

    def test_published_now(self, topic_fixture):
        '''
            Test if Topic is created with published_at field set to current datetime
        '''
        now = timezone.now()
        assert topic_fixture.published_at.date() == now.date(), 'Topic published_at date is not today'
        assert topic_fixture.published_at.time().hour == now.time().hour, 'Topic published_at hour should be now'
        assert topic_fixture.published_at.time().minute == now.time().minute, 'Topic published_at minute should be now'

'''
    Test Comment Model Behaviour
'''
class TestComment:

    def test_str(self, comment_fixture):
        assert str(comment_fixture) == comment_fixture.content[:10]

    def test_nbr_comments_increments(self, topic_fixture):
        '''
            Test Topic nbr_comments increases after
            adding comments to that Topic
        '''
        assert topic_fixture.nbr_comments == 0
        c1 = mommy.make('topics.Comment', topic=topic_fixture)
        assert topic_fixture.nbr_comments == 1
        c2 = mommy.make('topics.Comment', topic=topic_fixture)
        assert topic_fixture.nbr_comments == 2

    def test_nbr_comments_decrements(self, topic_fixture):
        '''
            Test Topic nbr_comments decreases after
            removing comments of that Topic
        '''
        assert topic_fixture.nbr_comments == 0
        c = mommy.make('topics.Comment', topic=topic_fixture)
        assert topic_fixture.nbr_comments == 1
        c.delete()
        assert topic_fixture.nbr_comments == 0

'''
    Test Upvote Model Behaviour
'''
class TestUpvote:
    
    def test_nbr_upvotes_increments(self, topic_fixture):
        '''
            Test Topic nbr_upvotes increases after
            adding upvotes to that Topic
        '''
        assert topic_fixture.nbr_upvotes == 0
        u1 = mommy.make('topics.Upvote', topic=topic_fixture)
        assert topic_fixture.nbr_upvotes == 1
        u2 = mommy.make('topics.Upvote', topic=topic_fixture)
        assert topic_fixture.nbr_upvotes == 2

    def test_nbr_upvotes_decrements(self, topic_fixture):
        '''
            Test Topic nbr_upvotes decreases after
            removing upvotes of that Topic
        '''
        assert topic_fixture.nbr_upvotes == 0
        u = mommy.make('topics.Upvote', topic=topic_fixture)
        assert topic_fixture.nbr_upvotes == 1
        u.delete()
        assert topic_fixture.nbr_upvotes == 0
