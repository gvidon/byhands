# -*- coding: utf-8 -*-
from django import forms

MESSAGES = {
	'invalid'   : u'Вы тут что-то не то напечатали',
	'required'  : u'Это нам обязательно нужно',
	'min_length': lambda length: u'Минимальная длина этого поля в символах '+str(length),
}

class OrderForm(forms.Form):
	name = forms.CharField(min_length=2, max_length=64, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})
	
	address = forms.CharField(min_length=2, max_length=255, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})
	
	city = forms.CharField(required=True, widget=forms.Select(choices=[
			(u'Ростов-на-Дону', u'Ростов-на-Дону'),
			(u'Краснодар'     , u'Краснодар'),
			(u'Москва'        , u'Москва'),
	], attrs={'class': 'special'}), error_messages={'required': MESSAGES['required']}, max_length=16)

	email = forms.EmailField(widget=forms.TextInput(attrs={
		'maxlength': 128
	}), error_messages={
		'required': MESSAGES['required'],
		'invalid' : MESSAGES['invalid'],
	})
	
	phone = forms.IntegerField(widget=forms.TextInput(attrs={
		'maxlength': 10
	}), error_messages={
		'invalid'  : u'Тут могут быть только 10 цифр (например 9181234567) без пробелов и без "-".',
		'required' : u'А где же телефон?',
	})
