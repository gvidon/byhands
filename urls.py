# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib            import admin

from contactus.views           import form
from tags.views                import search

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^/?$'    , form, name='contactus'),
	
	url(r'^search/', include('search.urls')),
	url(r'^shop/'  , include('candy.urls')),
	
	url(r'^(?P<type>(articles|products)?)/by\-tag/(?P<tag>[\w\-_\!\s]+)', search, name='by-tag'),
	
	url(r'^'       , include('accounts.urls')),
	url(r'^'       , include('pentackle.urls')),
	url(r'^'       , include('staticpages.urls')),
)

urlpatterns += patterns('',
	url('^admin/(.*)', admin.site.root),
)
