# -*- coding: utf-8 -*-
from datetime                        import date
from django.template.defaultfilters  import stringfilter
from django                          import template

register = template.Library()

#TRANSLATE ENG MONTH NAMES
@register.filter(name='ru_months')
@stringfilter
def ru_months(date, simple=None):
	try:
		return [
			date.replace(month[0], (simple and month[1] or month[2]))
			for month in months if date.find(month[0]) != -1
		][0]
	
	except IndexError:
		return ''
