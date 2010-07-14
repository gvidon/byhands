# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db                  import models

# ПОДПИСЧИКИ
class Subscriber(models.Model):
	email       = models.EmailField(max_length=124, unique=True, blank=True, null=True)
	user        = models.ForeignKey(User, unique=True, blank=True, null=True)
	
	canceled_at = models.DateTimeField(blank=True, null=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	
	cancel_code = models.CharField(max_length=64, blank=True, null=True)
	
	class Meta:
		db_table = 'subscriber'
	
	def __unicode__(self):
		return self.email or self.user.email
	
	def save(self, *args, **kwargs):
		import hashlib
		
		self.cancel_code = self.cancel_code or hashlib.md5(
			str(Subscriber.objects.all().count()) + self.email or self.user.email
		).hexdigest()
		
		return super(Subscriber, self).save(*args, **kwargs)

# СООБЩЕНИЯ списка рассылки
class Mail(models.Model):
	is_active  = models.BooleanField(default=False)
	subject    = models.CharField(max_length=124)
	body       = models.TextField()
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = 'mail'
	
	def __unicode__(self):
		return self.subject

# ЛОГ отправленных сообщений
class SentLog(models.Model):
	subscriber = models.ForeignKey(Subscriber, related_name='recieved_mails')
	mail       = models.ForeignKey(Mail, related_name='sent_to')
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = 'sent_log'
	
	def __unicode__(self):
		return self.mail.subject + ' -> ' + self.subscriber.email
