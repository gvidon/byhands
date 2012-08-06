# -*- coding: utf-8 -*-
from django.db import models

#CONTACTUS FORM MODEL
class ContactUs(models.Model):
	name          = models.CharField(max_length=100)
	city          = models.CharField(max_length=50, blank=False)
	
	email         = models.EmailField(max_length=100, blank=True)
	icq           = models.IntegerField(max_length=10, blank=True)
	phone         = models.CharField(max_length=15, blank=True)
	
	craft         = models.TextField(max_length=255)
	is_customable = models.BooleanField(default=False)
	
	#META
	class Meta:
		db_table = 'contacts'
