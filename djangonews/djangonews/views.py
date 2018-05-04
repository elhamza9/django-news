from django.shortcuts import redirect, render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import send_mail

from topics.models import Topic, Upvote, Comment
from django.contrib.auth.models import User
from djangonews.forms import UserForm

def welcome(request):
    return redirect('list_topics')

def profile(request):
    u =  request.user
    if not u.is_authenticated:
        raise Http404('Need to be authenticated')
    upvotes = Upvote.objects.filter(upvoter=u)
    nbr_upvotes = len(upvotes)
    comments = Comment.objects.filter(author=u)
    nbr_comments = len(comments)
    topics = Topic.objects.filter(author=u)
    nbr_topics = len(topics)
    user_info_form = UserForm(data={'username': u.get_username(), 'email': u.email, 'first_name': u.first_name, 'last_name': u.last_name})
    return render(request, 'auth/profile.html', {
                            'fullname': u.get_full_name(),
                            'user_info_form': user_info_form,
                            'nbr_topics': nbr_topics ,
                            'nbr_upvotes': nbr_upvotes,
                            'nbr_comments': nbr_comments,
                            'upvotes': upvotes,
                            'comments': comments,
                            'topics': topics})

def profile_change_basic_info(request):
    u = request.user
    if not u.is_authenticated:
        raise Http404('Need to be authenticated')
    form = UserForm(instance=u, data=request.POST)
    if form.is_valid():
        form.save()
    else:
        raise Http404('Form invalid')
    return redirect('profile')