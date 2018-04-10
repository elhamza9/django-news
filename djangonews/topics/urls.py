from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_topics, name='list_topics'),
    path('<str:slug>', views.detail_topic, name='detail_topic'),
    path('<int:id_topic>/comments', views.submit_comment, name='submit_comment')
]