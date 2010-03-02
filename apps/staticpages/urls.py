# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
	url(r'^how-to-order/?$'    , 'direct_to_template', {'template': 'staticpages/order.html'}     , name='how-to-order'),
	url(r'^individual-order/?$', 'direct_to_template', {'template': 'staticpages/individual.html'}, name='individual-order'),
	url(r'^shipping/?$'        , 'direct_to_template', {'template': 'staticpages/shipping.html'}  , name='shipping'),
	url(r'^payment/?$'         , 'direct_to_template', {'template': 'staticpages/payment.html'}   , name='payment'),
	url(r'^partner/?$'         , 'direct_to_template', {'template': 'staticpages/partner.html'}   , name='partner'),
	url(r'^rules/?$'           , 'direct_to_template', {'template': 'staticpages/rules.html'}     , name='rules'),
	url(r'^contacts/?$'        , 'direct_to_template', {'template': 'staticpages/contacts.html'}  , name='contacts'),
	url(r'^authors/?$'         , 'direct_to_template', {'template': 'staticpages/authors.html'}   , name='authors'),
)
