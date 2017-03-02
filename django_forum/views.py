from django.template import RequestContext
from django.forms import models as forms_models
from django.http import HttpResponseRedirect
from twitterapp.views import trend_results
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django_forum.models import Forum, Topic, Post
from django_forum.forms import TopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from trenditapp.settings import *
from datetime import datetime, timedelta


def index(request):
    """Main listing."""
    forums = Forum.objects.all()
    context = {'forums': forums, 'user': request.user}
    return render(request,"django_simple_forum/list.html", context)


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    num_items = 3
    paginator = Paginator(items, num_items)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


from twitterapp.views import trend_results
# def forum(request, forum_id):
#     """Listing of topics in a forum."""
#     # if request.method=='GET':
#     #         user_term = request.GET.get('searchterm')
#     #         print(user_term)
#     topics = Topic.objects.filter(forum=1).order_by("-created")
#     # user_term = request.GET.get('searchterm')
#     # topics = Topic.objects.filter(title__contains=user_term)
#     topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)
#
#     forum = get_object_or_404(Forum, pk=forum_id)
#     # context = {'searchterm':user_term}
#
#     return render(request,"django_simple_forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum),
#                               )


def forum(request, forum_id):
    """Listing of topics in a forum."""
    if request.method == 'GET':

        user_term1 = request.GET.get('searchterm',)
        print(user_term1)

        if user_term1 is not None:

            topics = Topic.objects.filter(title__contains=user_term1)
            topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

            forum = get_object_or_404(Forum, pk=forum_id)
# context = {'searchterm':user_term}

            return render(request, "django_simple_forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum, searchterm=user_term1),)

        else:
            now = datetime.now()
            time_threshold = now - timedelta(minutes=1)
            print(time_threshold)
            topics = Topic.objects.filter(created__range=(time_threshold,now))
            topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

            forum = get_object_or_404(Forum, pk=forum_id)
            return render(request,"django_simple_forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum, searchterm=user_term1),)


def topic(request, topic_id):
    """Listing of posts in a topic."""

    posts = Post.objects.filter(topic=topic_id).order_by("created")
    posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
    topic = Topic.objects.get(pk=topic_id)
    return render(request,"django_simple_forum/topic.html", add_csrf(request, posts=posts, pk=topic_id,
        topic=topic))


@login_required
def post_reply(request, topic_id):
    form = PostForm()
    topic = Topic.objects.get(pk=topic_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id,  )))

    return render(request,'django_simple_forum/reply.html', {
            'form': form,
            'topic': topic,
        })

@login_required
def new_topic(request, forum_id):
    form = TopicForm()
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.method=='GET':
        user_term2 = request.GET.get('searchterm',)
        print(user_term2)

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            # topic.title = user_term2
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('forum-detail', args=(forum_id)))

    return render(request,'django_simple_forum/new-topic.html', {
            'form': form,
            'forum': forum,
            'searchterm':user_term2,
        })
