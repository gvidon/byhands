# -*- coding: utf-8 -*-
from MySQLdb                    import IntegrityError

from django.contrib.auth.models import User
from postman.models             import Subscriber

# ОТКАЗ от рассылки
def cancel(request, code, confirmed=False):
	from django.template.context import RequestContext
	from django.shortcuts        import get_object_or_404
	from django.shortcuts        import render_to_response
	from datetime                import datetime
	
	subscriber = get_object_or_404(Subscriber, cancel_code=code)
	
	subscriber.canceled_at = datetime.today()
	subscriber.save()
	
	return render_to_response('postman/cancel.html', {
		'confirmed': confirmed,
		'code'     : code,
	}, context_instance=RequestContext(request))

# ПОДПИСАТЬ указанный email на рассылку апдейтов
def subscribe(request):
	from django.template.loader import render_to_string
	from django.core.validators import email_re
	from django.core.mail       import EmailMessage
	from django.http            import HttpResponse, Http404
	
	try:
		email = email_re.match(request.POST['email']).group(0)
		user  = User.objects.get(email=email)
	
	except AttributeError:
		return HttpResponse(u'{"success": 0, "error": "Неверный email"}')
		
	except User.DoesNotExist:
		user = None
	
	except KeyError:
		raise Http404
	
	try:
		msg = EmailMessage(u'Рассылка ByHands.ru', render_to_string('mail/subscribe-success.html', {
			'subscriber': Subscriber.objects.create(
				email = user and None or email,
				user  = user
			)
		}), 'do-not-reply@byhands.ru', [email,])
		
		msg.content_subtype = "html"
		msg.send()
	
	except IntegrityError:
		# Если эта подписка ранее анулирована - активировать снова
		try:
			subscriber = Subscriber.objects.filter(
				email = user and None or email,
				user  = user
			).exclude(canceled_at=None)[0]
			
			subscriber.canceled_at = None
			subscriber.save()
			
		except IndexError:
			return HttpResponse(u'{"success": 0, "error": "Этот email уже получает нашу рассылку"}')
			
	return HttpResponse('{"success": 1}')
