from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Topic, Comment
from .forms import CommentForm

from django.utils import timezone

# Create your views here.

def list_topics(request):
    topics = Topic.objects.all()
    return render(request, 'topics/list.html', {'topics': topics})
    '''
    titles = []
    for t in topics:
        titles.append(t.title)
    return HttpResponse('Here I list all topics: %s' % (' - '.join(titles)))
    '''

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
            'form': None if request.user.is_authenticated == False else CommentForm() })

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