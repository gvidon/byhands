# -*- coding: utf-8 -*-
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple     import direct_to_template
from django.conf.urls.defaults       import *
from django.contrib                  import admin
from django.conf                     import settings

from contactus.views                 import form
from tags.views                      import search

admin.autodiscover()
handler500 = 'staticpages.views.error_handler'

try:
	urlpatterns = patterns('', url('^admin(.*)', admin.site.root))
except AttributeError:
	urlpatterns = patterns('', url('^admin/', admin.site.urls))


urlpatterns += patterns('',
	url(r'^contactus/?$', form, name='contactus'),	
	url(r'^search/', include('search.urls')),
	
	url(r'^', include('postman.urls')),
	url(r'^', include('candy.urls')),
	url(r'^', include('staticpages.urls')),
	url(r'^', include('accounts.urls')),
	url(r'^', include('pentackle.urls')),
	
	url(r'^robots.txt$', direct_to_template, {'template': 'robots.txt'}, name='robots.txt'),
	url(r'^(?P<type>(articles|products)?)/by\-tag/(?P<tag>[\w\-_\!\s]+)', search, name='by-tag'),
)

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()
