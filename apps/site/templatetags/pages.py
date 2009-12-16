# -*- coding: utf-8 -*-
import re

from django.template.defaultfilters  import stringfilter
from django.conf                     import settings
from django                          import template

register = template.Library()

@register.inclusion_tag('common/_pages.html')
def pages(paginator, page_obj, url):
	
	# fuckin' calculations
	# int() / int() == int(int() / int())
	next_layer = ((page_obj.number - 1)/settings.MAX_SHOW_PAGES + 1) * settings.MAX_SHOW_PAGES + 1
	prev_layer = (page_obj.number - 1)/settings.MAX_SHOW_PAGES * settings.MAX_SHOW_PAGES
	
	return {
		'page_range' : paginator.page_range[prev_layer : next_layer -1],
		'num_page'   : paginator.num_pages,
		'count_items': paginator.count,
		'page_obj'   : page_obj,
		'many_pages' : paginator.num_pages > settings.MAX_SHOW_PAGES,
		'url'        : re.sub(r'/(page/[0-9]+/?)?$', '', url),
		
		'next_layer': {
			'start': next_layer <= paginator.num_pages and next_layer or 0,
			'end'  : next_layer + settings.MAX_SHOW_PAGES - 1 <= paginator.num_pages and next_layer + settings.MAX_SHOW_PAGES - 1 or paginator.num_pages,
		},
		
		'prev_layer': {
			'start': prev_layer - settings.MAX_SHOW_PAGES + 1,
			'end'  : prev_layer,
		}
	}
