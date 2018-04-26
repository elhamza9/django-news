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



class TestTopic:

    def test_list_topics_view(self, req_factory):
        '''
            Test list_topic view
        '''
        req = req_factory.get(reverse('site_index'))
        resp = views.list_topics(req)
        assert resp.status_code == 200

    def test_detail_topic(self, req_factory):
        '''
            Test Anonymous user access Detail Topic View
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.get(reverse('detail_topic',kwargs={'slug':t.slug}))
        req.user = AnonymousUser()
        resp = views.detail_topic(req, t.slug)
        assert resp.status_code == 200 , 'View Should return 200'

    def test_detail_non_existing_topic_raises_exception(self,req_factory):
        '''
            Test Http404 Exception gets raised when trying to access
            page of non existing topic ( slug part is wrong )
        '''
        wrong_slug = 'some-wrong-slug'
        req = req_factory.get(reverse('detail_topic',kwargs={'slug':wrong_slug}))
        req.user = AnonymousUser()
        with pytest.raises(Http404):
            resp = views.detail_topic(req, wrong_slug)

    def test_anonymous_add_topic_view_redirected_to_login(self, client):
        '''
            Test that anonymous user can't access add_topic view
        '''
        resp = client.get(reverse('add_topic'), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert last_url == reverse('user_login')

    def test_add_topic_view_authenticated(self, req_factory):
        '''
            Test that authenticated user can access add_topic view
        '''
        req = req_factory.get(reverse('add_topic'))
        req.user = mommy.make('User')
        resp = views.add_topic(req)
        assert resp.status_code == 200, 'View should return 200 because user is authenticated'

    def test_logged_can_post_topic(self, req_factory):
        '''
            Test that a logged user can add a topic
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy1', password=plain_pass)
        req = req_factory.post(reverse('add_topic'), data={
            'title': 'My Topic',
            'slug': 'my-topic',
            'content': 'My Awesome topic is great. upvote it !'
        })
        req.user = u
        resp = views.add_topic(req)
        assert Topic.objects.get(slug='my-topic')
    
    def test_logged_post_invalid_topic_exception(self, req_factory):
        '''
            Test that an exception get raised when a  logged user
            tries to submit a invalid form to add a topic
            (it should actually be prevented by javascript, but
            just in case)
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy1', password=plain_pass)
        req = req_factory.post(reverse('add_topic'), data={
            'title': 'My Topic',
            'slug': '', # No slug !
            'content': 'My Awesome topic is great. upvote it !'
        })
        req.user = u
        with pytest.raises(Http404):
            resp = views.add_topic(req)

class TestComment:

    def test_logged_user_submit_comment(self, req_factory):
        '''
            Test that a logged user can post a comment on a Topic
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy1', password=plain_pass)
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('submit_comment', kwargs={'id_topic': t.id}),
                data= {'content': 'My Comment'})
        req.user = u
        resp = views.submit_comment(req, t.id)
        assert Comment.objects.get(author=u)

    def test_user_cant_submit_empty_comment(self, req_factory):
        '''
            Test that a user cant post an empty comment on a Topic
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy2', password=plain_pass)
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('submit_comment', kwargs={'id_topic': t.id}),
                data= {'content': ''})
        req.user = u
        with pytest.raises(Http404):
            resp = views.submit_comment(req, t.id)


    def test_anonymous_comment_is_redirected_to_login(self, client):
        '''
            Test that anonymous user can't access add_topic view
        '''
        resp = client.post(reverse('submit_comment', kwargs={'id_topic': 0}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert last_url == reverse('user_login')

    def test_user_can_delete_his_comment(self, req_factory):
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

    def test_user_cant_delete_comment_of_another_user(self, req_factory):
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

    def test_anonymous_cant_delete_comment(self, req_factory):
        '''
            Test that 404 Exception gets raised when
            anonymous user tries to delete a comment
        '''
        c = mommy.make('topics.Comment')
        req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
        req.user = AnonymousUser()
        with pytest.raises(Http404):
            resp = views.delete_comment(req, c.id)

class TestUpvote:

    def test_logged_user_can_upvote_topic(self, req_factory):
        '''
            Test that a logged user can upvote a topic
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy2', password=plain_pass)
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = u
        resp = views.upvote_topic(req, t.id)
        assert Upvote.objects.get(upvoter=u)

    def test_anonymous_upvote_is_redirected_to_login(self, client):
        '''
            Test that anonymous user can't upvote
        '''
        t = mommy.make('topics.Topic')
        resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('user_login')

    def test_redirect_when_user_tries_to_upvote_two_times(self, client):
        '''
            Test that authenticated user will be redirected to topic page
            when he/she tries to upvote topic more than one time
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy2', password=plain_pass)
        t = mommy.make('topics.Topic')
        logged = client.login(username=u.get_username(), password=plain_pass)
        assert logged == True
        resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        assert resp.status_code == 200
        resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('detail_topic',kwargs={'slug': t.slug})

    def test_logged_user_can_cancel_upvote(self, req_factory):
        '''
            Test that logged user can cancel his upvote
            his upvote gets deleted from DB
        '''
        plain_pass = 'mysecurepass'
        u = User.objects.create_user(username='dummy2', password=plain_pass)
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = u
        resp = views.upvote_topic(req, t.id)
        assert Upvote.objects.get(upvoter=u)
        req = req_factory.post(reverse('cancel_upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = u
        resp = views.upvote_topic_cancel(req, t.id)
        with pytest.raises(ObjectDoesNotExist):
            assert Upvote.objects.get(upvoter=u)

    def test_anonymous_cancel_upvote_is_redirected_to_login(self, client):
        '''
            Test Anonymous user can't cancel upvote
        '''
        t = mommy.make('topics.Topic')
        resp = client.post(reverse('cancel_upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('user_login')
