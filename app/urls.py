# users/urls.py
from django.urls import path, include
from . import views
from django.conf.urls import url
import django.contrib.auth
from django.views.generic.base import TemplateView

urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    # path('/login', 'django.contrib.auth.login'),
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^reset/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset, name='reset'),
    url(r'^resetRequire/$', views.resetRequire, name='resetRequire'),
    url(r'^ha-noi/(?P<locationUrl>[0-9A-Za-z_\-]+)/$', views.location, name='location'),
    url(r'^search/$', views.search, name='search'),
    url(r'^like_create/$', views.like_create, name='like_create'),
    url(r'^like_decreate/$', views.like_decreate, name='like_decreate'),
    url(r'^view_create/$', views.view_create, name='view_create'),
    # url(r'^(?P<locationUrl>[0-9A-Za-z_\-/]+)/thuc-don/$', views.menu, name='menu'),

]
