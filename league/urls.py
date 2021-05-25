from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from .views import Table, index, login, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('table/', Table.as_view(), name='table'),
    path('', index),
    path('', include("django.contrib.auth.urls")),
    path('register/', register, name='register'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
