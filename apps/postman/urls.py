# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf               import settings

urlpatterns = patterns('postman.views',
	url(r'^unsubscribe/(?P<code>[\w\d]+)/confirmed/?$', 'cancel', {'confirmed': True} , name='unsubscribe-confirm'),
	url(r'^unsubscribe/(?P<code>[\w\d]+)/?$'          , 'cancel', {'confirmed': False}, name='unsubscribe'),
	
	url(r'^subscribe/?$'                              , 'subscribe', name='subscribe')
)

