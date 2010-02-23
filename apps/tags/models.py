# -*- coding: utf-8 -*-
from django.db import models

class Tag(models.Model):
	title = models.CharField(max_length=64)
		
	#СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title
	
	#META
	class Meta:
		db_table = 'tag'
