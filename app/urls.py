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
    url(r'^thanh-vien/(?P<userId>[0-9A-Za-z_\-]+)/$', views.member, name='member'),
    url(r'^search/$', views.search, name='search'),
    url(r'^like_create/$', views.like_create, name='like_create'),
    url(r'^like_decreate/$', views.like_decreate, name='like_decreate'),
    url(r'^view_create/$', views.view_create, name='view_create'),
    url(r'^share_create/$', views.share_create, name='share_create'),
    url(r'^collection_create/$', views.collection_create, name='collection_create'),
    url(r'^collection_delete/$', views.collection_delete, name='collection_delete'),
    url(r'^location_suggest/$', views.location_suggest, name='location_suggest'),
    url(r'^location_to_collection/$', views.location_to_collection, name='location_to_collection'),
    url(r'^get_collection/$', views.get_collection, name='get_collection'),
    url(r'^locations_in_collection/$', views.locations_in_collection, name='locations_in_collection'),
    url(r'^delete_location_in_collection/$', views.delete_location_in_collection, name='delete_location_in_collection'),
    # url(r'^(?P<locationUrl>[0-9A-Za-z_\-/]+)/thuc-don/$', views.menu, name='menu'),

]
