# -*- coding: utf-8 -*-
from datetime                       import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers       import reverse
from django.template.context        import RequestContext
from django.core.exceptions         import ValidationError

from django.views.generic           import list_detail
from django.core.mail               import mail_managers
from django.shortcuts               import render_to_response
from django.shortcuts               import get_object_or_404

from django.conf                    import settings
from django.http                    import HttpResponse, Http404

from models                         import Category, Order, OrderItem, Product
from forms                          import OrderForm

#ДОБАВЛЕНИЕ АЙТЕМА В КОРЗИНУ ПО ИДУ ПРОДУКТА
def add_item(request, id):
	cart = request.session.get('cart', {})
	
	try:
		cart[id].quantity += 1
		
	except KeyError:
		cart[id] = get_object_or_404(Product, pk=id)
		
		cart[id].quantity = 1
		cart[id].comment  = ''
	
	cart[id].sum = cart[id].price * float(cart[id].quantity)
	
	request.session['cart'] = cart
	
	if request.POST.get('simple'):
		return HttpResponse(str(reduce(
			lambda sum, (id,p): sum + (p.quantity * p.price),
		request.session['cart'].iteritems(), 0))+' p.')
	
	else:
		return render_to_response('candy/_cart-preview.html', context_instance=RequestContext(request))

#ОТМЕНА ЗАКАЗА
def cancel(request, id):
	order = get_object_or_404(Order, pk=id, is_delivered__in=(None, False))
	order.is_cancelled = True
	
	if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		return HttpResponse('{ success: 1 }')
	else:
		return HttpResponseRedirect(reverse('candy-orders'))

#ОБЗОР ЗАКАЗАННЫХ АЙТЕМОВ
def cart(request):
	return render_to_response('candy/cart.html', {
		'total': cart_total(request.session.get('cart') or {})
	}, context_instance=RequestContext(request))

#ОБЩАЯ ЦЕНА КОРЗИНЫ
def cart_total(cart):
	return sum([ float(item.quantity) * item.price for id, item in cart.iteritems() ])

#ОБЗОР КАТЕГОРИИ
def category(request, slug, page=None):
	for slug in slug.split('/'):
		category = get_object_or_404(Category, slug=slug, parent=locals().get('category'))
	
	return list_detail.object_list(request,
		queryset      = category.products.all(),
		paginate_by   = settings.ITEMS_PER_PAGE,
		page          = page,
		allow_empty   = True,
		template_name = 'candy/category.html',
		extra_context = { 'category': category }
	)

#ПОЛНОСТЬЮ ОЧИСТИТЬ КОРЗИНУ
def clear_cart(request):
	try:
		del(request.session['cart'])
	except KeyError:
		pass
	
	return HttpResponse('{ success: 1 }')

#СТРАНИЦА ТОПОВЫХ ТОВАРОВ
def featured(request):
	return render_to_response('candy/featured.html', {
		'featured_items': Product.objects.filter(is_featured=True).order_by('?')
	}, context_instance=RequestContext(request))

#ОБЗОР УСЛОВИЙ ЗАКАЗА И СОХРАНЕНИЕ
def order(request, id=None):
	try:
		# просмотр ранее завершенного заказа
		order = Order.objects.get(pk=id, user=request.user.is_authenticated() and request.user or None)
		
	except Order.DoesNotExist:
		
		# если корзина пуста заказа не будет
		if not request.session.get('cart'):
			raise Http404
		
		# использовать в форме заказа данные из последнего заказа
		try:
			last_order = Order.objects.filter(user=request.user).order_by('-id')[0]
		
		except IndexError:
			last_order = None
		
		try:
			form = OrderForm(auto_id='%s', initial={
				'name'   : request.user.first_name+' '+request.user.last_name,
				'email'  : request.user.email,
				'phone'  : request.user.get_profile().phone,
			
				'city'   : last_order and last_order.city,
				'address': last_order and last_order.address,
				'phone'  : last_order and last_order.phone
			})
		
		except AttributeError:
			form = OrderForm()
		
		if request.POST:
			form = OrderForm(request.POST, auto_id='%s')
			
			# сохранение заказа
			if form.is_valid():
				order = Order.objects.create(
					user         = request.user,
					name         = form.cleaned_data['name'],
					
					city         = form.cleaned_data['city'],
					address      = form.cleaned_data['address'],
					
					email        = form.cleaned_data['email'],
					phone        = form.cleaned_data['phone'],
					
					sum          = cart_total(request.session['cart']),
					is_confirmed = 1
				)
				
				for id, item in request.session['cart'].iteritems():
					OrderItem.objects.create(
						order        = order,
						product_id   = item.id,
						title        = item.title,
						quantity     = item.quantity,
						comment      = item.comment,
						price        = item.price,
						sum          = item.price * float(item.quantity)
					)
				
				del(request.session['cart'])
				
				mail_managers(u'Новый заказ номер '+str(order.id), unicode(
					'Поступил новый заказ на сумму '+str(order.sum)+' руб. Контактные данные: '+
					order.name+' ('+str(order.phone)+', '+order.email+'). Доставка по адрессу '+order.city+', '+
					order.address
				))
				
				return render_to_response('candy/order-confirmed.html', {'order': order}, context_instance=RequestContext(request))
				
	return render_to_response('candy/order.html', {
		'order': locals().get('order'),
		'form' : locals().get('form'),
		'items': locals().has_key('order') and order.items.all() or [item for id, item in request.session['cart'].iteritems()],
		'total': cart_total(request.session.get('cart') or {}),
	}, context_instance=RequestContext(request))

#СПИСОК УЖЕ СОВЕРШЕННЫХ ЗАКАЗОВ
@login_required
def orders(request):
	return render_to_response('candy/orders.html', {
		'orders': Order.objects.filter(user=request.user, is_confirmed=True).order_by('-id'),
	}, context_instance=RequestContext(request))
	
	return list_detail.object_list(request,
		queryset      = Order.objects.filter(user=request.user, is_confirmed=True),
		allow_empty   = True,
		template_name = 'candy/orders.html'
	)

#СТРАНИЦА ПРОДУКТА
def product(request, category, product):
	print settings.MEDIA_URL
	
	try:
		history = bool(request.META['HTTP_REFERER'].find('/shop') + 1) and request.META['HTTP_REFERER']
	except KeyError:
		pass
	
	return render_to_response('candy/product.html', {
		'product': get_object_or_404(Product, category__slug=category, slug=product),
		'history': locals().get('history'),
	}, context_instance=RequestContext(request))

#УДАЛИТЬ АЙТЕМ ИЗ КОРЗИНЫ
def remove_item(request, id):
	try:
		cart = request.session.get('cart', {})
		del(cart[id])
		request.session['cart'] = cart
		
		return HttpResponse('{ success: 1, price: "%.2f" }'%cart_total(cart))
		
	except KeyError:
		raise Http404

#ОБНОВИТЬ КОЛИЧЕСТВО АЙТЕМОВ КОРЗИНЫ
def update_cart(request):
	cart = request.session['cart']
	
	# в POST хэш с ключами вида q34, c78 и т.д.
	try:
		for id, value in request.POST.iteritems():
			
			# если устанвливает значение количества, то привести к целому
			cart[id[1:]].__setattr__({
				'q': 'quantity',
				'c': 'comments',
			}[id[0]], id[0] == 'q' and int(value) or value)
			
			cart[id[1:]].sum = cart[id[1:]].price * float(cart[id[1:]].quantity)
		
		request.session['cart'] = dict(filter(lambda i: int(i[1].quantity) > 0, cart.iteritems()))
	
	except KeyError:
		return HttpResponse(u'{ success: 0, message: "Ошибка обработки запроса. Попробуйте обновить страницу." }')
	
	except ValueError:
		raise Http404
	
	return HttpResponse('{success: 1, price: '+str(cart_total(request.session['cart']))+'}')
