# -*- coding: utf-8 -*-
from datetime                 import datetime
from django.core.urlresolvers import reverse
from django.conf              import settings
from django                   import template

from apps.candy.models        import Category, Order, Product

register = template.Library()

#ДЕРЕВО КАТЕГОРИЙ МАГАЗИНА
@register.simple_tag
def categories_tree(current=None):
	# делает список категорий со вложенными подкатегориями
	def tree(categories, parents):
		for category in categories:
			if category in parents:
				categories.insert(categories.index(category) + 1, list(Category.objects.filter(parent=category)))
				
			elif isinstance(category, list):
				categories[categories.index(category)] = tree(category, parents)
		
		return categories
	
	# рендерит дерево
	def render(tree, current, sub=False):
		return '<ul class="%s">%s</ul>'%(sub and 'left_submenu' or '', ('').join(['<li>%s</li>'%(
			isinstance(category, list) and render(category, current, True)
				or '<a href="%s" class="%s">%s</a>'%(
					reverse('candy-category', args=[category.path()]),
					category == current and 'active' or '',
					category.title
				)
		) for category in tree if category]))
	
	try:
		parents = [current]
		
		for parent in parents:
			parents.append(parent.parent)
		
	except (AttributeError, Category.DoesNotExist):
		return render(tree(
			list(Category.objects.filter(parent=None)), locals().get('parents', [])
		), current)

#ПУТЬ ИЗ КОРНЯ КАТЕГОРИЙ К ТЕКУЩЕЙ
@register.inclusion_tag('candy/_category-parents.html')
def category_parents(current, product=None):
	
	media_url = settings.MEDIA_URL
	
	try:
		parents = [current]
		
		for parent in parents:
			parents.append(parent.parent)
		
	except (AttributeError, Category.DoesNotExist):
		parents.reverse()
		return locals()

#КРАТКАЯ СВОДКА ПО ПРЕДЫДУЩИМ ЗАКАЗАМ
@register.inclusion_tag('candy/_orders-preview.html')
def orders_preview(count, user_id):
	return {'orders': Order.objects.filter(user=user_id, is_confirmed=True).order_by('-id')[:count]}
