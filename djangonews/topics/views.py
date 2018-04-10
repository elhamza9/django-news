from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from .models import Topic, Comment, Upvote
from .forms import CommentForm, UpvoteForm

from django.utils import timezone

# Create your views here.

def list_topics(request):
    sorting_type = request.GET.get('sort', 'recent')
    if sorting_type == 'recent' or (sorting_type != 'recent' and sorting_type != 'rated') :
        topics = Topic.objects.all()
    else:
        topics = Topic.objects.all()
        
    return render(request, 'topics/list.html', {'topics': topics})

def detail_topic(request, slug=''):
    try:
        assert len(slug) > 0
        res = Topic.objects.filter(slug=slug)
        assert len(res) == 1
    except AssertionError:
        raise Http404("Article Not Found !")

    topic = res[0]
    return render(request, 'topics/detail.html',{
            'title': topic.title, 
            'published_at': topic.published_at ,
            'content': topic.content,
            'id': topic.id,
            'comments': topic.comments.all(),
            'nbr_upvotes': len(topic.upvotes.all()),
            'nbr_comments': len(topic.comments.all()),
            'upvoted': True,
            'comment_form': None if request.user.is_authenticated == False else CommentForm(),
            'upvote_form': None if request.user.is_authenticated == False else UpvoteForm() })

def submit_comment(request, id_topic=0):
    try:
        assert request.method == 'POST'
    except AssertionError:
        raise Http404("Wrong Method")
    
    topic = get_object_or_404(Topic, pk=id_topic)
    author = request.user
    comment = Comment(author=author, topic=topic, published_at=timezone.now())
    form = CommentForm(instance=comment, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('list_topics')
    else:
        raise Http404('Form invalid')


def upvote_topic(request, id_topic=0):
    try:
        assert request.method == 'POST'
    except AssertionError:
        raise Http404("Wrong Method")

    topic = get_object_or_404(Topic, pk=id_topic)
    user = request.user
    
    try:
        res = Upvote.objects.filter(Q(topic=topic) & Q(upvoter=user))
        assert len(res) == 0
    except AssertionError:
        return redirect('detail_topic', slug=topic.slug)
    
    upvote = Upvote(upvoter=user, topic=topic, timestamp=timezone.now())
    form = UpvoteForm(instance=upvote, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('detail_topic', slug=topic.slug)
    else:
        raise Http404('Form invalid')