from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Topic, Comment, Upvote
from .forms import TopicForm, CommentForm, UpvoteForm

from django.utils import timezone

# Create your views here.

def list_topics(request):
    sorting_type = request.GET.get('sort', 'recent')
    if sorting_type == 'recent' or (sorting_type != 'recent' and sorting_type != 'rated') :
        sorting_type = 'recent'
        topic_list = Topic.objects.all()
    else:
        topic_list = Topic.objects.order_by('-nbr_upvotes')

    # Pagination
    paginator = Paginator(topic_list, 20)
    page_count = paginator.num_pages
    page = request.GET.get('page', '0')
    if int(page) > page_count:
        raise Http404('No more pages')

    topics_page = paginator.get_page(page)
    if int(page) == 0:
        return render(request, 'topics/list.html', {'topics': topics_page, 'page_count': page_count, 'sort_type': sorting_type})
    else:
        return JsonResponse(list(topics_page.object_list.values()), safe=False)

def detail_topic(request, slug=''):
    try:
        assert len(slug) > 0
        res = Topic.objects.filter(slug=slug)
        assert len(res) == 1
    except AssertionError:
        raise Http404("Article Not Found !")

    topic = res[0]
    user = request.user or None
    if user != None and user.is_authenticated == True:
        res = Upvote.objects.filter(Q(topic=topic) & Q(upvoter=user))
        assert len(res) in (0,1)
        user_upvoted_topic = len(res) == 1
    else:
        user_upvoted_topic = False
        
    return render(request, 'topics/detail.html',{
            'title': topic.title, 
            'published_at': topic.published_at ,
            'content': topic.content,
            'id': topic.id,
            'author_name': topic.author.get_username(),
            'comments': topic.comments.all(),
            'nbr_upvotes': topic.nbr_upvotes,
            'nbr_comments': topic.nbr_comments,
            'upvoted': user_upvoted_topic,
            'upvote_form_url': 'upvote_topic' if user_upvoted_topic == False else 'cancel_upvote_topic',
            'comment_form': None if request.user.is_authenticated == False else CommentForm(),
            'upvote_form': None if request.user.is_authenticated == False else UpvoteForm() })

def submit_comment(request, id_topic=0):
    try:
        assert request.method == 'POST'
    except AssertionError:
        raise Http404("Wrong Method")

    try:
        assert request.user.is_authenticated == True
    except AssertionError:
        return redirect('user_login')

    topic = get_object_or_404(Topic, pk=id_topic)
    author = request.user
    comment = Comment(author=author, topic=topic, published_at=timezone.now())
    form = CommentForm(instance=comment, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('detail_topic', slug=topic.slug)
    else:
        raise Http404('Form invalid')

def delete_comment(request, id_comment=0):
    print('ID comment : {}'.format(id_comment))
    comment = get_object_or_404(Comment, id=id_comment)
    try:
        assert comment.author == request.user
    except AssertionError:
        raise Http404('Not the same user who commented')
    comment.delete()
    return redirect('detail_topic', slug=comment.topic.slug)


def upvote_topic(request, id_topic=0):
    try:
        assert request.method == 'POST'
    except AssertionError:
        raise Http404("Wrong Method")

    user = request.user
    try:
        assert user.is_authenticated == True
    except AssertionError:
        return redirect('user_login')

    topic = get_object_or_404(Topic, pk=id_topic)
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

def upvote_topic_cancel(request, id_topic=0):
    topic = get_object_or_404(Topic, pk=id_topic)
    res = Upvote.objects.filter(Q(topic=topic) & Q(upvoter=request.user))
    assert len(res) == 1
    res[0].delete()
    return redirect('detail_topic', slug=topic.slug)

def add_topic(request):
    try:
        assert request.user.is_authenticated == True
    except AssertionError:
        return redirect('user_login')

    if request.method == 'POST':
        topic = Topic(author=request.user)
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('site_index')
        return HttpResponse('Posting a Topic')
    elif request.method == 'GET':
        form = TopicForm()
        return render(request, 'topics/form.html', {'action': 'Add', 'form': form})
    else:
        raise Http404('Wrong Method')