from django.shortcuts import redirect, render
from django.http import Http404
from topics.models import Topic, Upvote, Comment

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
    return render(request, 'auth/profile.html', {'username': u.get_username(),
                            'nbr_topics': nbr_topics ,
                            'nbr_upvotes': nbr_upvotes,
                            'nbr_comments': nbr_comments,
                            'upvotes': upvotes,
                            'comments': comments,
                            'topics': topics})
