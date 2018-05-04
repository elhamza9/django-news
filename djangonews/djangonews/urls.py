"""djangonews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import views as auth_views

from . import views
from topics.views import list_topics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('topics/', include('topics.urls')),
    path('login', LoginView.as_view(template_name='auth/login.html'), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),
    path('oauth/', include('social_django.urls', namespace='social')),  # for Facebook Auth
    path('tinymce/', include('tinymce.urls')),
    path('profile/', views.profile, name='profile'),
    path('profile/change/basic-info', views.profile_change_basic_info, name='profile_change_basic_info'),
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('',list_topics, name='site_index')
]
