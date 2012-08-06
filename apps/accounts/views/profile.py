# -*- coding: utf-8 -*-
import hashlib, random, httplib, urllib
from PIL import Image

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from django.template.context        import RequestContext
from django.shortcuts               import render_to_response
from django.conf                    import settings

from accounts.forms                 import ProfileForm
from accounts.models                import Profile

#USER PROFILE FORM
@login_required
def form(request):
	profile = Profile.objects.get(user=request.user)
	
	form = ProfileForm(auto_id='%s', initial={
		'id'        : request.user.id,
		'username'  : request.user.username,
		'email'     : request.user.email,
		'avatar'    : profile.avatar,
		
		'first_name': request.user.first_name,
		'sur_name'  : profile.sur_name,
		'last_name' : request.user.last_name,
		
		'gender'    : profile.gender,
		'birthdate' : profile.birthdate,
		
		'phone'     : profile.phone,
		'icq'       : profile.icq,
	})
	
	if request.POST:
		form = ProfileForm(auto_id='%s', data=request.POST, files=request.FILES)
		
		if(form.is_valid()):
			# update user info and profile
			User.objects.filter(id=request.user.id).update(
				username   = form.cleaned_data.get('username'),
				email      = form.cleaned_data.get('email'),
				first_name = form.cleaned_data.get('first_name'),
				last_name  = form.cleaned_data.get('last_name')
			)
			
			Profile.objects.filter(id=request.user.get_profile().id).update(
				user      = request.user,
				avatar    = request.FILES and 'upload/avatars/'+str(request.user.id) or '',
				sur_name  = form.cleaned_data.get('sur_name'),
				gender    = form.cleaned_data.get('gender'),
				birthdate = form.cleaned_data.get('birthdate'),
				phone     = form.cleaned_data.get('phone'),
				icq       = form.cleaned_data.get('icq')
			)
			
			# resize and save uploaded avatar
			if request.FILES:
				filename = settings.UPLOAD_ROOT+'avatars/'+str(request.user.id)
				
				avatar = open(filename,'wb+')
				for chunk in request.FILES['avatar'].chunks(): avatar.write(chunk)
				avatar.close()
				
				image = Image.open(filename)
				
				if image.mode not in ('L', 'RGB'):
					image = image.convert('RGB')
				
				image.thumbnail((70, 70), Image.ANTIALIAS)
				image.save(filename, image.format)
				
				Profile.objects.filter(id=form.cleaned_data.get('id')).update(
					avatar='upload/avatars/'+str(request.user.id)
				)
			
			profile = Profile.objects.get(user=request.user)
				
	return render_to_response('accounts/profile.html', {
		'form'   : form,
		'profile': profile,
	}, context_instance=RequestContext(request))
