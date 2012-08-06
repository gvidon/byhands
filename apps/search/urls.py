# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views                     import process

urlpatterns = patterns('',
	url(r'^$', process, name='search'),
)

