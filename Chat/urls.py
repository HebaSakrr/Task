# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views

app_name = 'Chat'
urlpatterns = [
               url(r'^$', views.signin, name='signin'),
               url(r'^signup/$', views.signup, name='signup'),
               url(r'^contacts/$', views.contacts, name='contacts'),
               url(r'^chating/$', views.chating, name='chating'),
]
