# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf               import settings
from models                    import Article

#ОБЗОР БЛОГА
urlpatterns = patterns('pentackle.views',
    url(r'^(?P<slug>[\-\d\w]+)/?(page/(?P<page>[0-9]+)/?)?$', 'articles', name='blogposts')
)

#АРХИВ РАЗДЕЛА
urlpatterns += patterns('pentackle.views',
    url(r'^(?P<slug>[\-\d\w]+)/archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive', name='archive')
)

#ПРОСМОТР СТАТЬИ
urlpatterns += patterns('django.views.generic.list_detail', url(r'^article/(?P<slug>[\-\d\w]+)/$', 'object_detail', {
	'slug_field'   : 'slug',
	'queryset'     : Article.objects.all(),
}, name='article'))
