# -*- coding: utf-8 -*-
import hashlib, random, re

from django.contrib.auth.models import User
from django.template.loader     import render_to_string
from models                     import Profile, Activation

def register_inactive(username, email, first_name='', last_name='', surname=None):
	# create DISABLED user
	user = User.objects.create_user(username, email, '')
	
	user.first_name = first_name
	user.last_name  = last_name
	user.is_active  = 0
	
	user.save()
	
	# populate user's profile
	Profile.objects.create(
		user      = user,
		auth_type = 'local',
		sur_name  = surname
	)
	
	# prepare activation code
	md5hash = hashlib.md5()
	md5hash.update(str(user.id+int(random.random()*50)))
	
	Activation.objects.create(
		user  = user,
		type  = 'email',
		value = email,
		code  = md5hash.hexdigest()
	)
	
	# send HTML email to newly registered user
	#user.get_profile().send_email('Активация учетной записи на byhands.ru',
	#	render_to_string('mail/register.html', { 'code': md5hash.hexdigest() }).encode('utf8')
	#)
	
	return user
