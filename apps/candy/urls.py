# -*- coding: utf-8 -*-
from django.views.generic.list_detail import object_detail
from django.conf.urls.defaults        import *
from django.conf                      import settings

from models                           import Category, Product
from views                            import *

urlpatterns = patterns('',
	# главная - топовые товары и лист категорий
	url(r'^/?$'                                                         , featured   , name='candy'),
	
	# просмотр и управление корзиной
	url(r'^cart/?$'                                                    , cart       , name='candy-cart'),
	
	url(r'^cart/add/(?P<id>[0-9]+)/?$'                                 , add_item   , name='candy-add-item'),
	url(r'^cart/remove/(?P<id>[0-9]+)/?$'                              , remove_item, name='candy-remove-item'),
	url(r'^cart/clear/?$'                                              , clear_cart , name='candy-clear-cart'),
	url(r'^cart/update/?$'                                             , update_cart, name='candy-update-cart'),
	
	# заказы
	url(r'^order/?$'                                                   , order      , name='candy-create-order'),
	url(r'^order/(?P<id>[0-9]+)/?$'                                    , order      , name='candy-view-order'),
	url(r'^order/(?P<id>[0-9]+)/cancel/?$'                             , cancel     , name='candy-cancel'),
	
	url(r'^orders/?$'                                                  , orders     , name='candy-orders'),
	
	# серфинг по каталогу
	url(r'^category/(?P<slug>[\w\d\-_\/]+)/page/(?P<page>[0-9]+)/?$'   , category   , name='candy-category-page'),
	url(r'^category/(?P<slug>[\w\d\-_\/]+)/$'                          , category   , name='candy-category'),
	
	url(r'^product/(?P<category>[\w\d\-_]+)/(?P<product>[\w\d\-_]+)/?$', product    , name='candy-product'),
)

