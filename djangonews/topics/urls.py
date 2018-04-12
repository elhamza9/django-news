from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_topics, name='list_topics'),
    path('new', views.add_topic, name='add_topic'),
    path('<str:slug>', views.detail_topic, name='detail_topic'),
    path('<int:id_topic>/comments', views.submit_comment, name='submit_comment'),
    path('comments/<int:id_comment>/delete', views.delete_comment, name='delete_comment'),
    path('<int:id_topic>/upvote', views.upvote_topic, name='upvote_topic'),
    path('<int:id_topic>/upvote/cancel', views.upvote_topic_cancel, name='cancel_upvote_topic'),
]