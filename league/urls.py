from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from .views import Table, index, login, register, team, Matches, profile, match

urlpatterns = [
    path('admin/', admin.site.urls),
    path('table/', Table.as_view(), name='table'),
    path('', Table.as_view(), name='table'),
    path('match/', Matches.as_view(), name='match'),
    path('', index),
    path('', include("django.contrib.auth.urls")),
    path('register/', register, name='register'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('table/team/', team, name='team'),
    url(r'^table/team/(?P<team_id>[0-9]+)/$', team, name='team'),
    path('table/team/profile/', profile, name='profile'),
    url(r'^table/team/profile/(?P<profile_id>[0-9]+)/$', profile, name='profile'),
    path('match/details/', match, name='match'),
    url(r'^match/details/(?P<match_id>[0-9]+)/$', match , name='match')
]
