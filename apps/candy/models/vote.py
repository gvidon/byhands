# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db                  import models

#РЕЙТИНГ НА МАНЕР НРАВИТСЯ/НЕ НРАВИТСЯ
class Vote(models.Model):
	user       = models.ForeignKey(User, blank=True, null=True)
	product    = models.ForeignKey('Product')
	created_at = models.DateTimeField(auto_now_add=True)
	ip         = models.IPAddressField()
	
	#META
	class Meta:
		app_label           = 'candy'
		db_table            = 'vote'
		verbose_name        = u'Голос'
		verbose_name_plural = u'Голоса'
