from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Topic

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
            'content': topic.content})