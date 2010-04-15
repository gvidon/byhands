# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.conf              import settings

from pentackle.models         import Article

#КЛЮЧ С НАЗВАНИЕМ ТЕКУЩЕГО РАЗДЕЛА ИМЕЕТ ЗНАЧЕНИЕМ ACTIVE
def active_section(request):
	view, args, kwargs = resolve(request.path)
	
	try:
		return { 'active_section': { dict((
			# список постов и архив
			map(lambda F: (F, lambda kwargs: kwargs['slug']), ('articles', 'archive')) +
			
			# просмотр поста
			map(lambda F:
				(F, lambda kwargs: Article.objects.get(slug=kwargs['slug']).sections.all()[0].slug),
				('object_detail',)) +
		
			# просмотр статических страниц
			map(lambda F:
				(F, lambda kwargs: kwargs['template'].replace('staticpages/', '').replace('.html', '')),
				('direct_to_template',)
			) +
			
			# серфинг по магазину
			map(lambda F: (F, lambda kwargs: 'shop'), (
				'featured', 'cart', 'category', 'order', 'orders', 'product'
			))
		))[view.__name__](kwargs): 'active' } }
	
	except KeyError:
		return {}

#ОБЩАЯ ЦЕНА КОРЗИНЫ
def cart(request):
	try:
		return {
			'cart': reduce(lambda sum, (id, p): {
				'quantity': sum['quantity'] + p.quantity,
				'price'   : sum['price'] + p.quantity * p.price
			}, request.session['cart'].iteritems(), {'quantity': 0, 'price': 0}),
		}
	
	except KeyError:
		return {'cart': {'quantity': 0, 'price': 0}}

#MEDIA SERVER URL
def media_url(request):
	return { 'media_url': settings.MEDIA_URL }

#МЕТА ДАННЫЕ ДЛЯ URL-А
def meta(request):
	from seo.models import Meta
	
	try:
		meta = Meta.objects.get(url=request.META['PATH_INFO'])
		return { 'META_KEYWORDS': meta.keywords, 'META_DESCRIPTION': meta.description }
	
	except Meta.DoesNotExist:
		return {}

