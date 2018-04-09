

from django.urls import path

from . import views

urlpatterns = [
	path('', views.index),
    path('new/', views.topic_submit),
    path('<str:slug>/', views.topic_detail),
    path('<int:id>/upvote', views.topic_upvote),
    path('<int:id>/comment', views.topic_comment)
]