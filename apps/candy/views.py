# -*- coding: utf-8 -*-
from datetime                       import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
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
from apps.accounts.utils            import register_inactive

#ДОБАВЛЕНИЕ АЙТЕМА В КОРЗИНУ ПО ИДУ ПРОДУКТА
def add_item(request, id):

	if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
		return render_to_response('manual-order.html', context_instance=RequestContext(request))
	
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
	
	# если категория пуста и есть дочерние - взять первую дочернюю
	if not category.products.all() and Category.objects.filter(parent=category).count():
		category = Category.objects.filter(parent=category).order_by('priority')[0]
	
	return list_detail.object_list(request,
		queryset      = category.products.order_by('-created_at').all(),
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

# ЕКСПОРТ данных в формате YML http://help.yandex.ru/partnermarket/?id=1111425
def export_yandex(request):
	from datetime               import datetime
	from django.template.loader import render_to_string
	from models                 import Category
	
	return HttpResponse(render_to_string('candy/export-yandex.xml', {
		'categories': Category.objects.only('id', 'parent', 'title').select_related('parent__id', 'parent__title'),
		'now'       : datetime.now().strftime('%Y-%m-%d %H:%M'),
		
		'items': Product.objects.only(
			'id', 'title', 'description', 'price', 'slug'
		).select_related(
			'category', 'photos'
		),
	}), mimetype='text/xml')

#СТРАНИЦА ТОПОВЫХ ТОВАРОВ
def featured(request):
	return render_to_response('candy/featured.html', {
		'featured_items': Product.objects.filter(is_featured=True).order_by('?')[:8]
	}, context_instance=RequestContext(request))

#ОБЗОР УСЛОВИЙ ЗАКАЗА И СОХРАНЕНИЕ
def order(request, id=None):
	
	DELIVERIES = { 'post': 230, 'ems': 550, 'pek': 350, 'self': 0 }
	
	try:
		# просмотр ранее завершенного заказа
		order = Order.objects.get(pk=id, user=request.user.is_authenticated() and request.user or None)
		
	except Order.DoesNotExist:
		
		# если корзина пуста заказа не будет
		if not request.session.get('cart'):
			raise Http404
		
		# использовать в форме заказа данные из последнего заказа
		try:
			last_order = Order.objects.filter(
				user = request.user.is_authenticated() and request.user or None
			).order_by('-id')[0]
		
		except IndexError:
			last_order = None
		
		try:
			form = OrderForm(auto_id='%s', initial={
				'name'   : request.user.first_name+' '+request.user.last_name,
				'email'  : request.user.email,
				'phone'  : request.user.get_profile() and request.user.get_profile().phone or None,
				'city'   : last_order and last_order.city,
				'address': last_order and last_order.address,
				'phone'  : last_order and last_order.phone
			})
		
		except AttributeError:
			form = OrderForm(auto_id='%s')
		
		if request.POST:
			form = OrderForm(request.POST, auto_id='%s')
			
			try:
				user = User.objects.get(email=request.POST['email'])
				
				# если клиент не авторизован и использует мыльник действительного
				# аккаунта из базы - поругаться и предложить авторизоваться
				if not request.user.is_authenticated():
					auth_error = True
				
			except User.DoesNotExist:
				if form.is_valid():
					user = register_inactive(
						form.cleaned_data['email'][0:form.cleaned_data['email'].index('@')],
						form.cleaned_data['email']
					)
			
			# такое может быть с пользователя, с пустым email
			except User.MultipleObjectsReturned:
				pass
			
			# сохранение заказа
			if form.is_valid() and not locals().get('auth_error'):
				
				for values in [form.cleaned_data]:
					order = Order.objects.create(
						user         = user,
						name         = values['name'],
						
						city         = values['city'],
						address      = values['address'],
						
						email        = values['email'],
						phone        = values['phone'],
						
						delivery_by  = values['delivery_by'],
						sum          = cart_total(request.session['cart']) + DELIVERIES[values['delivery_by']],
						is_confirmed = 1,
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
				
				items_str = (', ').join([u'"%s" x %s (%.2f р. всего)' % (
					item.title,
					item.quantity,
					float(item.quantity) * item.price
				) for id, item in request.session['cart'].iteritems()])
				
				user.get_profile().send_email(u'Заказ номер %i принят к обработке' % order.id, (u'''
					Вы совершили заказ на сумму %(sum).2f рублей. Контактные данные: %(name)s,
					email %(email)s, телефон %(phone)s. Доставка по адресу %(city)s, %(address)s.
					
					Содержимое заказа: %(items)s.
					
					Спасибо, мы свяжемся с вами в ближайшее время!
				''' % {
					'address': order.address,
					'phone'  : order.phone,
					'email'  : order.email,
					'city'   : order.city,
					'name'   : order.name,
					'sum'    : order.sum,
					'items'  : items_str,
				}).encode('utf8'))
				
				del(request.session['cart'])
				
				mail_managers(u'Новый заказ номер '+str(order.id),
					u'Поступил новый заказ на сумму '+str(order.sum)+u' руб. Контактные данные: '+
					order.name+' ('+str(order.phone)+', '+order.email+u'). Доставка по адрессу '+order.city+', '+
					order.address + u'. Способ доставки '+order.delivery_by+u'. Содержимое заказа: ' + items_str
				)
				
				return render_to_response('candy/order-confirmed.html', {'order': order}, context_instance=RequestContext(request))
	
	return render_to_response('candy/order.html', {
		'order'     : locals().get('order'),
		'form'      : locals().get('form'),
		'auth_error': locals().get('auth_error'),
		'total'     : cart_total(request.session.get('cart') or {}),
		'delivery'  : DELIVERIES[locals().get('order') and order.delivery_by or request.POST.get('delivery_by', 'post')],
		'deliveries': DELIVERIES,
		
		'items': locals().has_key('order') and order.items.all() or [
			item for id, item in request.session['cart'].iteritems()
		],
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
	try:
		history = bool(request.META['HTTP_REFERER'].find('/shop') + 1) and request.META['HTTP_REFERER']
	except KeyError:
		pass
	
	product = get_object_or_404(Product, category__slug=category, slug=product)
	
	return render_to_response('candy/product.html', {
		'category': product.category.get(slug=category),
		'product' : product,
		'history' : locals().get('history'),
	}, context_instance=RequestContext(request))

#УДАЛИТЬ АЙТЕМ ИЗ КОРЗИНЫ
def remove_item(request, id):
	try:
		cart = request.session.get('cart', {})
		del(cart[id])
		request.session['cart'] = cart
		
		return HttpResponse('{ "success": 1, "price": "%.2f" }'%cart_total(cart))
		
	except KeyError:
		raise Http404

#ОБНОВИТЬ КОЛИЧЕСТВО АЙТЕМОВ КОРЗИНЫ
def update_cart(request):
	cart = request.session['cart']
	
	# в POST хэш с ключами вида q34, c78 и т.д.
	try:
		for id, value in filter(lambda P: P[0] != 'csrfmiddlewaretoken', request.POST.iteritems()):
			
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
	
	return HttpResponse('{"success": 1, "price": '+str(cart_total(request.session['cart']))+'}')
