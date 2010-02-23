# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.shortcuts        import render_to_response
from pentackle.models        import Article

type2list = {
	'articles': [Article.objects.filter(publish=True), 'pentackle/article_list.html'],
}

#ПОИСК ПО БАЗЕ ТЭГОВ
def search(request, type, tag):
	return render_to_response(type2list[type][1], {
		'tag'        : tag,
		'object_list': type2list[type][0].filter(tags__title=tag)
	}, context_instance=RequestContext(request))
