# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.shortcuts        import render_to_response

from accounts.forms          import ProfileForm
from accounts.utils          import register_inactive

#REGISTER USER'S INFO AND SEND CONFIRMATION LINK
def form(request):
	form = ProfileForm(auto_id='%s')
	
	if request.POST:
		form = ProfileForm(auto_id='%s', data=request.POST)
		
		if(form.is_valid()):
			return render_to_response('accounts/register/thanx.html', { 'email': register_inactive(
				form.cleaned_data['username'],
				form.cleaned_data['email'],
				form.cleaned_data['first_name'],
				form.cleaned_data['last_name'],
				form.cleaned_data['sur_name'],
			).email }, context_instance=RequestContext(request))
	
	return render_to_response(
		'accounts/register/form.html',
		{'form': form},
		context_instance=RequestContext(request)
	)
