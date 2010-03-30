# -*- coding: utf-8 -*-
import re, smtplib

from email.mime.multipart       import MIMEMultipart
from email.mime.text            import MIMEText

from django.conf                import settings
from django.contrib.auth.models import User
from django.db                  import models

#ADDITIONAL USER ATTRIBUTES AND FLAGS
class Profile(models.Model):
	user      = models.ForeignKey(User)
	avatar    = models.ImageField(upload_to='upload/avatars', blank=True, null=True)
	
	auth_type = models.CharField(max_length=6, choices=(
		('Local' , 'local'),
		('OpenId', 'openid'),
	), blank=True, default='local')
	
	sur_name  = models.CharField(max_length=64, blank=True, null=True)
	
	gender    = models.CharField(max_length=6, choices=[
		('male', u'Мужской'), ('female', u'Женский')
	], blank=True, null=True)
	
	birthdate = models.DateTimeField(blank=True, null=True)
	phone     = models.CharField(max_length=16, blank=True, null=True)
	icq       = models.CharField(max_length=16, blank=True, null=True)
	
	#SEND CUSTOM EMAIL FROM SYSTEM TO USER
	def send_email(self, subject, message):
		msg = MIMEMultipart('alternative')
		msg.set_param('charset', 'utf-8')
		
		msg['Subject'] = subject
		msg['From']    = 'do-not-reply@byhands.ru'
		msg['To']      = self.user.email
		
		msg.attach(MIMEText(re.sub(r'<.*?>', '', message), _subtype='plain', _charset = 'utf-8'))
		msg.attach(MIMEText(message, _subtype='html' , _charset = 'utf-8'))
		
		s = smtplib.SMTP('localhost')
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		s.quit()
		
	class Meta:
		db_table = 'profile'

#ACTIVATION VALUES
class Activation(models.Model):
	user          = models.ForeignKey(User)
	value         = models.CharField(max_length=64)
	code          = models.CharField(max_length=64)
	
	request_date  = models.DateTimeField(auto_now_add=True)
	confirm_date  = models.DateTimeField(blank=True, null=True)
	
	type          = models.CharField(max_length=8, choices=(
		('Password', 'password'),
		('Email'   , 'email'),
		('Phone'   , 'phone')
	), default='email')
	
	class Meta:
		db_table = 'activation'

	
