# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms               import ModelForm
from django                     import forms
from models                     import Profile

MESSAGES = {
	'invalid'   : u'Вы тут что-то не то напечатали',
	'required'  : u'Это нам обязательно нужно',
	'min_length': lambda length: u'Минимальная длина этого поля в символах '+str(length),
}

#FIELD VALUE LENGTH VALIDATION FUNCTION
def assert_length(value, length):
	try:
		return filter(lambda value: len(str(value)) == length, [value])[0]
	
	except IndexError:
		raise forms.ValidationError(u'Неверное количество цифр, должно быть '+str(length))

#ADDITIONAL USER ATTRIBUTES AND FLAGS
class ProfileForm(forms.Form):

	id         = forms.IntegerField(required=False, widget=forms.HiddenInput())

	username   = forms.CharField(min_length=2, max_length=64, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})

	email      = forms.EmailField(widget=forms.TextInput(attrs={
		'maxlength': 128
	}), error_messages={
		'required': MESSAGES['required'],
		'invalid' : MESSAGES['invalid'],
	})

	avatar     = forms.ImageField(required=False, error_messages={
		'invalid_image': u'Это не похоже на картинку',
		'invalid'      : MESSAGES['invalid'],
	})

	first_name = forms.CharField(required=False, min_length=2, max_length=64, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})
	
	sur_name   = forms.CharField(required=False, min_length=2, max_length=64, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})
	
	last_name  = forms.CharField(required=False, min_length=2, max_length=64, error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	})
	
	birthdate  = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={
		'maxlength': 20
	}), error_messages={
		'required': MESSAGES['required'],
		'invalid' : MESSAGES['invalid'],
	})
	
	gender     = forms.CharField(required=False, widget=forms.Select(
		choices=[('male', u'Папа'), ('female', u'Мама')]
	), error_messages={
		'required'  : MESSAGES['required'],
		'min_length': MESSAGES['min_length'](2),
	}, min_length=4, max_length=6)
	
	phone      = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
		'maxlength': 10
	}), error_messages={
		'invalid'  : u'Тут могут быть только цифры без пробелов и без "-".',
	})
	
	icq        = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
		'maxlength': 12
	}), error_messages={
		'invalid'  : u'Тут могут быть только цифры без пробелов и без "-".',
	})
	
	#CHECK USERNAME FOR UNIQUENESS
	def clean_username(self):
		
		# не пускать пробелы
		if self.cleaned_data['username'].find(' ') >= 0:
			raise forms.ValidationError(u'Имя пользователя не может содержать пробелов.')
		
		# проверить на уникальность
		try:
			User.objects.exclude(id=self.cleaned_data['id']).get(username=self.cleaned_data['username'])
			
			raise forms.ValidationError(u'Пользователь с таким псевдонимом уже есть в нашей базе.')
			
		except User.DoesNotExist:
			return self.cleaned_data['username']
	
	#CHECK EMAIL FOR UNIQUENESS
	def clean_email(self):
		try:
			User.objects.exclude(id=self.cleaned_data['id']).get(email=self.cleaned_data['email'])
			
			raise forms.ValidationError(
				u'Такой email уже есть в базе. Хотите <a href="/user/recover">восстановить пароль</a> ?'
			)
			
		except User.DoesNotExist:
			return self.cleaned_data['email']
	
	#VALIDATE ICQ NUM LENGTH
	def clean_icq(self):
		if self.cleaned_data.get('icq'):
			return assert_length(self.cleaned_data.get('icq'), 12)
	
	#VALIDATE PHONE LENGTH
	def clean_phone(self):
		if self.cleaned_data.get('phone'):
			return assert_length(self.cleaned_data.get('phone'), 10)
