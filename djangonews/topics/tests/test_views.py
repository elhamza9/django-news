import pytest

from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist

from model_mommy import mommy

from topics import views
from topics.models import Topic, Comment, Upvote

pytestmark = pytest.mark.django_db

@pytest.fixture
def req_factory():
    return RequestFactory()

@pytest.fixture
def client():
    return Client()



@pytest.mark.skip
def test_list_topics_recent():
    assert 1 == 0

@pytest.mark.skip
def test_list_topics_rated():
    assert 1 == 0

def test_detail_topic(req_factory):
    '''
        Test Anonymous user access Detail Topic View
    '''
    t = mommy.make('topics.Topic')
    req = req_factory.get(reverse('detail_topic',kwargs={'slug':t.slug}))
    req.user = AnonymousUser()
    resp = views.detail_topic(req, t.slug)
    assert resp.status_code == 200 , 'View Should return 200'

def test_add_topic_anonymous_redirect_to_login(client):
    '''
        Test that anonymous user can't access add_topic view
    '''
    resp = client.get(reverse('add_topic'), follow=True)
    last_url, code = resp.redirect_chain[-1]
    assert last_url == reverse('user_login')

def test_add_topic_authenticated(req_factory):
    '''
        Test that authenticated user can access add_topic view
    '''
    req = req_factory.get(reverse('add_topic'))
    req.user = mommy.make('User')
    resp = views.add_topic(req)
    assert resp.status_code == 200, 'View should return 200 because user is authenticated'

def test_comment_submit_anonymous_redirect_to_login(client):
    '''
        Test that anonymous user can't access add_topic view
    '''
    resp = client.post(reverse('submit_comment', kwargs={'id_topic': 0}), follow=True)
    last_url, code = resp.redirect_chain[-1]
    assert last_url == reverse('user_login')

def test_user_can_delete_his_comment(req_factory):
    '''
        Test that user can delete his own comment
    '''
    u = mommy.make('User')
    c = mommy.make('topics.Comment', author=u)
    req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
    req.user = u
    resp = views.delete_comment(req, c.id)
    #assert resp.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Comment.objects.get(id=c.id)

def test_user_cant_delete_comment_of_another_user(req_factory):
    '''
        Test that 404 Exception gets raised when
        user tries to delete another one's comment
    '''
    users = mommy.make('User', _quantity=2)
    c = mommy.make('topics.Comment', author=users[0])
    req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
    req.user = users[1]
    with pytest.raises(Http404):
        resp = views.delete_comment(req, c.id)

def test_anonymous_cant_delete_comment(req_factory):
    '''
        Test that 404 Exception gets raised when
        anonymous user tries to delete a comment
    '''
    c = mommy.make('topics.Comment')
    req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
    req.user = AnonymousUser()
    with pytest.raises(Http404):
        resp = views.delete_comment(req, c.id)


def test_anonymous_upvote_is_redirected_to_login(client):
    '''
        Test that anonymous user can't upvote
    '''
    t = mommy.make('topics.Topic')
    resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
    last_url, code = resp.redirect_chain[-1]
    assert code == 302
    assert last_url == reverse('user_login')

def test_redirect_when_user_tries_to_upvote_two_times(client):
    '''
        Test that authenticated user will be redirected to topic page
        when he/she tries to upvote topic more than one time
    '''
    plain_pass = 'mysecurepass'
    u = User.objects.create_user(username='dummy', password=plain_pass)
    t = mommy.make('topics.Topic')
    logged = client.login(username=u.get_username(), password=plain_pass)
    assert logged == True
    resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
    assert resp.status_code == 200
    resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
    last_url, code = resp.redirect_chain[-1]
    assert code == 302
    assert last_url == reverse('detail_topic',kwargs={'slug': t.slug})
