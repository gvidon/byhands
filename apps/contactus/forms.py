# -*- coding: utf-8 -*-
import re

from django import forms
from models import ContactUs

#CONTACTUS FORM
class ContactUsForm(forms.ModelForm):
	name = forms.CharField(max_length=100, error_messages={
		'required': u'<span class="error">Нам нужно знать ваше имя</span>',
	}, widget=forms.TextInput(attrs={ 'maxlength': '100' }))
	
	city = forms.CharField(max_length=100, error_messages={
		'required': u'<span class="error">В каком городе вы живете?</span>',
	}, widget=forms.TextInput(attrs={ 'maxlength': '100' }))
	
	icq = forms.IntegerField(required=False, error_messages={
		'invalid': u'<span class="error">Это не похоже на icq...</span>',
	}, widget=forms.TextInput(attrs={ 'maxlength': '11' }))
	
	email = forms.EmailField(required=False, error_messages={
		'invalid': u'<span class="error">Такие email не бывают, точно</span>',
	}, widget=forms.TextInput(attrs={ 'maxlength': '100' }))
	
	craft = forms.CharField(widget=forms.Textarea, max_length=255, error_messages={
		'required': u'<span class="error">А чем Вы занимаетесь?</span>',
	})
	
	#CHECK FOR ICQ, PHONE OR EMAIL EXISTING
	def clean(self):
		for contact in ('icq', 'phone', 'email'):
			if self.cleaned_data.get(contact):
				return self.cleaned_data
		
		raise forms.ValidationError(
			'Нам обязательно нужен <strong>один из Ваших контактов</strong> - icq, телефон или e-mail'
		)
	
	#PHONE VALIDATION
	def clean_phone(self):
		if not re.match(r'^\+?[ 0-9]{,15}$', self.cleaned_data['phone']):
			raise forms.ValidationError(u'Пример телефона: 8 911 123 45 67(только цифры, пробелы и "+")')
		
		return self.cleaned_data['phone']
	
	class Meta:
		model = ContactUs
