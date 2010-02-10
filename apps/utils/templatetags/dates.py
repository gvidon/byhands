# -*- coding: utf-8 -*-
from django.template.defaultfilters  import stringfilter
from datetime                        import date
from django                          import template

# Attach 3 characters month name to the list
months = [month + [month[0][0:3]] for month in [
	[ 'January'  , u'Январь'  , u'Января'   ],
	[ 'February' , u'Февраль' , u'Февраля'  ],
	[ 'March'    , u'Март'    , u'Марта'    ],
	[ 'April'    , u'Апрель'  , u'Апреля'   ],
	[ 'May'      , u'Май'     , u'Мая'      ],
	[ 'June'     , u'Июнь'    , u'Июня'     ],
	[ 'July'     , u'Июль'    , u'Июля'     ],
	[ 'August'   , u'Август'  , u'Августа'  ],
	[ 'September', u'Сентябрь', u'Сентября' ],
	[ 'October'  , u'Октябрь' , u'Октября'  ],
	[ 'November' , u'Ноябрь'  , u'Ноября'   ],
	[ 'December' , u'Декабрь' , u'Декабря'  ],
]]

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
