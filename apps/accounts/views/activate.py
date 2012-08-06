# -*- coding: utf-8 -*-
import hashlib, random, datetime

from django.template.loader      import render_to_string
from django.shortcuts            import render_to_response
from django.contrib.auth         import login
from django.contrib.auth.models  import User
from django.template.context     import RequestContext

from accounts.models             import Profile, Activation

#GET ACTIVATION CODE BY URL
def by_url(request, code):
	if confirm(request, code):
		return render_to_response('accounts/activate/thanx.html', context_instance=RequestContext(request))
	else:
		return render_to_response('accounts/activate/wrong-code.html', context_instance=RequestContext(request))

#CONFIRM ACTIVATION AND LOGIN USER
def confirm(request, code):
	if not Activation.objects.filter(code=code, confirm_date=None).count():
		return 0
	
	for contact in Activation.objects.filter(code=code):
		try:
			# activate and set confirm_date to today date
			contact.user.is_active = 1
			(contact.response_date, contact.confirm_date) = [datetime.datetime.today()] * 2
			contact.save()
			
			# set user password if confirming activation request
			if contact.user.password == '!':
				password = generate_password(contact.user.id)
				
				contact.user.set_password(password)
				contact.user.save()
				
				contact.user.get_profile().send_email('Учетная запись активирована',
					render_to_string('mail/activate.html', {
						'username': contact.user.username,
						'password': password,
					}).encode('utf8')
				)
			
			contact.user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, contact.user)
			
			contact.delete()
			
		except User.DoesNotExist:
			return 0
		
	return 1

#PASSWORD GENERATION ROUTINE
def generate_password(id):
	md5hash = hashlib.md5()
	md5hash.update(str(id+int(random.random()*50)))
	
	return md5hash.hexdigest()[:8]
