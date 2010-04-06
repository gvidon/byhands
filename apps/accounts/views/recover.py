# -*- coding: utf-8 -*-
import hashlib
import random
import re

from datetime                    import datetime

from django.contrib.auth.models  import User
from django.template.loader      import render_to_string
from django.shortcuts            import render_to_response
from django.http                 import Http404
from django.template             import RequestContext

from accounts.models             import Profile
from accounts.models             import Activation

#ПОДТВЕРЖДЕНИЕ ВОССТАНОВЛЕНИЯ ПАРОЛЯ
def confirm(request, code):
	try:
		activation = Activation.objects.get(code=code, type='password', confirm_date=None)
		
		plain_password = hashlib.md5(str(random.random())).hexdigest()[:8]
		
		activation.user.set_password(plain_password)
		activation.user.save()
		
		activation.user.get_profile().send_email('Новый пароль учетной записи',
			render_to_string('mail/recover-confirmed.html', {
				'login'   : activation.user.username,
				'password': plain_password,
			}).encode('utf8')
		)
		
		activation.response_date = datetime.today()
		activation.confirm_date = datetime.today()
		activation.save()
		
	except Activation.DoesNotExist:
		raise Http404
		
	return render_to_response('accounts/recover/thanx.html', {
		'email': activation.user.email
	}, context_instance=RequestContext(request))

#EMAIL FORM FOR PASSWORD CONFIRMATION
def form(request):
	if request.POST:
		try:
			user = User.objects.get(email=request.POST['email'] or request.POST['raise-keyerror'])
			code = hashlib.md5(str(random.random())).hexdigest()
			
			Activation.objects.create(user=user, type='password', code=code)
			
			user.get_profile().send_email('Восстановление пароля учетной записи',
				render_to_string('mail/recover.html', { 'code': code }).encode('utf8')
			)
			
		except KeyError:
			error = u'А где же e-mail?'
		
		except User.DoesNotExist:
			error = u'Учетной записи с таким e-mail нет в нашей базе.'
	
	return render_to_response('accounts/recover/form.html', {
		'error': locals().get('error', '')
	}, context_instance=RequestContext(request))
