# -*- coding: utf-8 -*-
import smtplib

from django.template.context import RequestContext
from django.shortcuts        import render_to_response
from forms                   import ContactUsForm

#CONTACTUS MAIN FORM
def form(request):
	form = ContactUsForm(auto_id='%s')
	
	if request.POST:
		form = ContactUsForm(auto_id='%s', data=request.POST)
		
		if form.is_valid():
			form.save()
			
			server = smtplib.SMTP('localhost')
			
			server.sendmail('From: no-reply@byhands.ru', 'To: info@byhands.ru',
				'Subject: еще один хэндмейдер\r\n'+
				request.POST['name'].encode('utf8')+' из '+request.POST['city'].encode('utf8')+'\n\n'
				
				'Контакты: '+(', ').join([
					type+': '+request.POST[type] for type in ['icq', 'email', 'phone'] if request.POST[type]
				]).encode('utf8')+'\n\n'+
				
				'Интересен тем, что'+'\n'+request.POST['craft'].encode('utf8')+'\n\n'+
				'Может на заказ!'*int(request.POST.has_key('is_customable') and 1 or 0)
			)
			
			server.quit()
			
			return render_to_response('contactus/thankyou.html', context_instance=RequestContext(request))
	
	return render_to_response('contactus/index.html', { 'form': form }, context_instance=RequestContext(request))
	
