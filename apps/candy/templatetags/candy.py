# -*- coding: utf-8 -*-
from datetime          import datetime

from django.conf       import settings
from django            import template

from apps.candy.models import Category, Order

register = template.Library()

@register.inclusion_tag('candy/_categories-tree.html')
def categories_tree(current):
	return { 'categories': Category.objects.all(), 'current': current }

@register.inclusion_tag('candy/_orders-preview.html')
def orders_preview(count, user_id):
	return {'orders': Order.objects.filter(user=user_id, is_confirmed=True).order_by('-id')[:count]}
