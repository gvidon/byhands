# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail       import EmailMessage
from djboss.commands        import *
from postman.models         import Mail, SentLog, Subscriber

@command
def send_updates(args):
	for mail in Mail.objects.filter(is_active=1):
		for subscriber in Subscriber.objects.exclude(recieved_mails__mail=mail).filter(canceled_at=None):
			if mail.created_at >= subscriber.created_at:
				
				msg = EmailMessage(mail.subject,
					render_to_string('mail/mail-list.html', { 'body': mail.body, 'subscriber': subscriber }),
					'do-not-reply@byhands.ru',
					[subscriber.user and subscriber.user.email or subscriber.email,]
				)
				
				msg.content_subtype = 'html'
				msg.send()
				
				SentLog.objects.create(mail=mail, subscriber=subscriber)
