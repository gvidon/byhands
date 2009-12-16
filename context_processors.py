# -*- coding: utf-8 -*-
from django.conf import settings

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
	
#SEPARATE MEDIA SERVER URL
def media_url(request):
	return { 'media_url': settings.MEDIA_URL }
