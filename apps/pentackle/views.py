# -*- coding: utf-8 -*-
from django.views.generic import date_based, list_detail
from django.http          import Http404
from django.conf          import settings

from models               import Article, Section

def archive(request):
	try:
		section = Section.objects.get(slug__exact=slug)
	
	except Section.DoesNotExist:
		raise Http404
		
	return date_based.archive_month(request,
		date_field    = 'pub_date',
		allow_empty   = True,
		queryset      = section.articles.filter(publish=True),
		template_name = 'pentackle/article_list.html',
		extra_context = { 'section': section },
	)

def articles(request, slug, page=1):
	try:
		section = Section.objects.get(slug__exact=slug)
	
	except Section.DoesNotExist:
		raise Http404
	
	return list_detail.object_list(request,
		queryset      = section.articles.filter(publish=True),
		paginate_by   = settings.ITEMS_PER_PAGE,
		page          = page,
		allow_empty   = True,
		template_name = 'pentackle/article_list.html',
		extra_context = { 'section': section },
	)
