# users/urls.py
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),

    path('', views.index, name='index'),
    url(r'^login/$', views.admin_login, name='admin_login'),
    # url(r'^signup/$', views.signup, name='signup'),
    # url(r'^activate/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    #
    url(r'^location/$', views.location, name='location'),
    url(r'^location/add/$', views.add_location, name='add_location'),
    url(r'^location/(?P<id>[0-9A-Za-z_\-]+)/binh-luan/$', views.comment, name='comment'),
    url(r'^location/(?P<id>[0-9A-Za-z_\-]+)/bai-do-xe/$', views.parking, name='parking'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user/(?P<id>[0-9A-Za-z_\-]+)/$', views.user, name='user'),
    path('success', views.success, name='success'),
    url(r'^get_required_message/$', views.get_required_message, name='get_required_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
