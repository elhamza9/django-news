from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='topics_list'),
    path('new/', views.topic_submit, name='topic_add'),
    path('<str:slug>/', views.topic_detail, name='topic_detail'),
    path('<int:id>/upvote', views.topic_upvote, name='topic_upvote'),
    path('<int:id>/comment', views.topic_comment, name='topic_comment')
]