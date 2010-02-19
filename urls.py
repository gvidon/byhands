# -*- coding: utf-8 -*-
from django.conf.urls.defaults    import *
from django.contrib               import admin

from byhands.apps.contactus.views import form

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^/?$'    , form, name='contactus'),
	url(r'^search/', include('search.urls')),
	url(r'^shop/'  , include('candy.urls')),
	url(r'^blog/'  , include('pentackle.urls')),
	url(r'^'       , include('accounts.urls')),
)

urlpatterns += patterns('',
	url('^admin/(.*)', admin.site.root),
)
