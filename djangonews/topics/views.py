from django.shortcuts import render
from django.http import HttpResponse

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