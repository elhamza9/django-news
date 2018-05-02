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

@pytest.fixture(scope="module")
def req_factory():
    return RequestFactory()

@pytest.fixture(scope="module")
def client():
    return Client()

plain_pass = 'mysecurepass'
@pytest.fixture
def registered_user():
    return User.objects.create_user(username='dummy', password=plain_pass)

@pytest.fixture(scope="module")
def anonymous_user():
    return AnonymousUser()


class TestTopic:

    def test_list_topics_view(self, req_factory, anonymous_user):
        '''
            Test list_topic view
        '''
        req = req_factory.get(reverse('site_index'))
        req.user = anonymous_user
        resp = views.list_topics(req)
        assert resp.status_code == 200

    def test_detail_topic_view(self, req_factory, anonymous_user):
        '''
            Test Anonymous user access Detail Topic View
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.get(reverse('detail_topic',kwargs={'slug':t.slug}))
        req.user = anonymous_user
        resp = views.detail_topic(req, t.slug)
        assert resp.status_code == 200 , 'View Should return 200'

    def test_edit_topic_view(self, req_factory, registered_user):
        pass

    def test_detail_topic_wrong_slug_raises_exception(self,req_factory, anonymous_user):
        '''
            Test Http404 Exception gets raised when trying to access
            page of non existing topic ( slug part is wrong )
        '''
        wrong_slug = 'some-wrong-slug'
        req = req_factory.get(reverse('detail_topic',kwargs={'slug':wrong_slug}))
        req.user = anonymous_user
        with pytest.raises(Http404):
            resp = views.detail_topic(req, wrong_slug)

    def test_anonymous_add_topic_view_redirected_to_login(self, client):
        '''
            Test that anonymous user can't access add_topic view
        '''
        resp = client.get(reverse('add_topic'), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert last_url == reverse('user_login')
        assert code == 302

    def test_logged_can_see_add_topic_view(self, req_factory, registered_user):
        '''
            Test that authenticated user can access add_topic view
        '''
        req = req_factory.get(reverse('add_topic'))
        req.user = registered_user
        resp = views.add_edit_topic(req)
        assert resp.status_code == 200, 'View should return 200 because user is authenticated'

    def test_logged_can_post_topic(self, req_factory, registered_user):
        '''
            Test that a logged user can add a topic
        '''
        req = req_factory.post(reverse('add_topic'), data={
            'title': 'My Topic',
            'slug': 'my-topic',
            'content': 'My Awesome topic is great. upvote it !'
        })
        req.user = registered_user
        resp = views.add_edit_topic(req)
        assert Topic.objects.get(slug='my-topic')

    def test_logged_post_invalid_topic_exception(self, req_factory, registered_user):
        '''
            Test that an exception get raised when a  logged user
            tries to submit a invalid form to add a topic
            (it should actually be prevented by javascript, but
            just in case)
        '''
        req = req_factory.post(reverse('add_topic'), data={
            'title': 'My Topic',
            'slug': '', # No slug !
            'content': 'My Awesome topic is great. upvote it !'
        })
        req.user = registered_user
        with pytest.raises(Http404):
            resp = views.add_edit_topic(req)
    
    def test_logged_can_edit_his_topic(self, req_factory, registered_user):
        '''
            Test that logged user can edit a topic he posted
        '''
        topic = mommy.make('topics.Topic', author=registered_user)
        previous_title = topic.title
        new_title = 'My Edited Topic'
        req = req_factory.post(reverse('edit_topic', kwargs={'id_topic': topic.id}), data={
            'title': new_title,
            'slug': 'my-edited-topic',
            'content': 'My Awesome topic is great. upvote it !'
            })
        req.user = registered_user
        resp = views.add_edit_topic(req, topic.id)
        topic = Topic.objects.get(id=topic.id)
        assert topic.title != previous_title and topic.title == new_title
    
    def test_logged_cant_edit_anothers_topic(self, req_factory, registered_user):
        '''
            Test that logged user can't edit a topic he didn't post
        '''
        other_user = User.objects.create_user(username='other', password='otherpassword')
        topic = mommy.make('topics.Topic', author=other_user)
        req = req_factory.post(reverse('edit_topic', kwargs={'id_topic': topic.id}), data={
            'title': 'My Edited Topic',
            'slug': 'my-edited-topic',
            'content': 'My Awesome topic is great. upvote it !'
            })
        req.user = registered_user
        with pytest.raises(Http404):
            resp = views.add_edit_topic(req, topic.id)


    def test_logged_can_delete_his_topic(self, req_factory, registered_user):
        '''
            Test that logged user can delete topic he posted
        '''
        topic = mommy.make('topics.Topic', author=registered_user)
        req = req_factory.get(reverse('delete_topic', kwargs={'id_topic': topic.id}))
        req.user = registered_user
        resp = views.delete_topic(req, topic.id)
        with pytest.raises(ObjectDoesNotExist):
            Topic.objects.get(id=topic.id)
    
    def test_logged_cant_delete_anothers_topic(self, req_factory, registered_user):
        '''
            Test that logged user can't delete a topic of another user
        '''
        other_user = User.objects.create_user(username='other', password='otherpassword')
        topic = mommy.make('topics.Topic', author=other_user)
        req = req_factory.get(reverse('delete_topic', kwargs={'id_topic': topic.id}))
        req.user = registered_user
        with pytest.raises(Http404):
            resp = views.delete_topic(req, topic.id)

class TestComment:

    def test_logged_can_submit_comment(self, req_factory, registered_user):
        '''
            Test that a logged user can post a comment on a Topic
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('submit_comment', kwargs={'id_topic': t.id}),
                data= {'content': 'My Comment'})
        req.user = registered_user
        resp = views.submit_comment(req, t.id)
        assert Comment.objects.get(author=registered_user)

    def test_logged_cant_submit_empty_comment(self, req_factory, registered_user):
        '''
            Test that a user cant post an empty comment on a Topic
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('submit_comment', kwargs={'id_topic': t.id}),
                data= {'content': ''})
        req.user = registered_user
        with pytest.raises(Http404):
            resp = views.submit_comment(req, t.id)


    def test_anonymous_submit_comment_redirected_to_login(self, client):
        '''
            Test that anonymous user can't access add_topic view
        '''
        resp = client.post(reverse('submit_comment', kwargs={'id_topic': 0}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert last_url == reverse('user_login')

    def test_logged_can_delete_his_comment(self, req_factory, registered_user):
        '''
            Test that user can delete his own comment
        '''
        c = mommy.make('topics.Comment', author=registered_user)
        req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
        req.user = registered_user
        resp = views.delete_comment(req, c.id)
        #assert resp.status_code == 200
        with pytest.raises(ObjectDoesNotExist):
            Comment.objects.get(id=c.id)

    def test_logged_cant_delete_comment_of_another_user(self, req_factory, registered_user):
        '''
            Test that 404 Exception gets raised when
            user tries to delete another one's comment
        '''
        other_user = mommy.make('User')
        c = mommy.make('topics.Comment', author=other_user)
        req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
        req.user = registered_user
        with pytest.raises(Http404):
            resp = views.delete_comment(req, c.id)

    def test_anonymous_cant_delete_comment(self, req_factory, anonymous_user):
        '''
            Test that 404 Exception gets raised when
            anonymous user tries to delete a comment
        '''
        c = mommy.make('topics.Comment')
        req = req_factory.get(reverse('delete_comment', kwargs={'id_comment': c.id}))
        req.user = anonymous_user
        with pytest.raises(Http404):
            resp = views.delete_comment(req, c.id)

class TestUpvote:

    def test_logged_can_upvote_topic(self, req_factory, registered_user):
        '''
            Test that a logged user can upvote a topic
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = registered_user
        resp = views.upvote_topic(req, t.id)
        assert Upvote.objects.get(upvoter=registered_user)

    def test_anonymous_upvote_is_redirected_to_login(self, client):
        '''
            Test that anonymous user can't upvote
        '''
        t = mommy.make('topics.Topic')
        resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('user_login')

    def test_redirect_when_logged_upvotes_or_cancels_upvote(self, client, registered_user):
        '''
            Test that authenticated user will be redirected to topic page
            when he/she tries to upvote topic more than one time
        '''
        t = mommy.make('topics.Topic')
        logged = client.login(username=registered_user.get_username(), password=plain_pass)
        assert logged == True
        resp = client.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('detail_topic',kwargs={'slug': t.slug})
        resp = client.post(reverse('cancel_upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('detail_topic',kwargs={'slug': t.slug})

    def test_logged_user_can_cancel_upvote(self, req_factory, registered_user):
        '''
            Test that logged user can cancel his upvote
            his upvote gets deleted from DB
        '''
        t = mommy.make('topics.Topic')
        req = req_factory.post(reverse('upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = registered_user
        resp = views.upvote_topic(req, t.id)
        assert Upvote.objects.get(upvoter=registered_user)
        req = req_factory.post(reverse('cancel_upvote_topic', kwargs={'id_topic': t.id}), data={})
        req.user = registered_user
        resp = views.upvote_topic_cancel(req, t.id)
        with pytest.raises(ObjectDoesNotExist):
            assert Upvote.objects.get(upvoter=registered_user)

    def test_anonymous_cancel_upvote_redirected_to_login(self, client):
        '''
            Test Anonymous user can't cancel upvote
        '''
        t = mommy.make('topics.Topic')
        resp = client.post(reverse('cancel_upvote_topic', kwargs={'id_topic': t.id}), follow=True)
        last_url, code = resp.redirect_chain[-1]
        assert code == 302
        assert last_url == reverse('user_login')
