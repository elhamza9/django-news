import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from model_mommy import mommy

from topics import views

pytestmark = pytest.mark.django_db

@pytest.fixture
def req_factory():
    return RequestFactory()


def test_list_topics_recent():
    assert 1 == 0

def test_list_topics_rated():
    assert 1 == 0

def test_detail_topic(req_factory):
    '''
        Test Detail Topic View
    '''
    t = mommy.make('topics.Topic')
    req = req_factory.get(reverse('detail_topic',kwargs={'slug':t.slug}))
    resp = views.add_topic(req)
    assert resp.status_code == 200 , 'View Should return 200'

def test_add_topic_anonymous_redirect_to_login(req_factory):
    '''
        Test that anonymous user can't access add_topic view
    '''
    req = req_factory.get(reverse('add_topic'))
    req.user = AnonymousUser()
    resp = views.add_topic(req)
    assert 'login' in resp.url , 'View should redirect us to login'

def test_add_topic_authenticated(req_factory):
    '''
        Test that authenticated user can access add_topic view
    '''
    req = req_factory.get(reverse('add_topic'))
    req.user = mommy.make('User')
    resp = views.add_topic(req)
    assert resp.status_code == 200, 'View should return 200 because user is authenticated'

def test_comment_submit_anonymous_redirect_to_login(req_factory):
    '''
        Test that anonymous user can't submit comment
    '''
    req = req_factory.get(reverse('submit_comment', kwargs={'id_topic':t.id}))
    req.user = AnonymousUser()
    resp = views.submit_comment(req)
    assert 'login' in resp.url , 'View should redirect us to login'

def test_comment_delete():
    assert 1 == 0

def test_upvote_submit_anonymous_redirect_to_login(req_factory):
    assert 1 == 0