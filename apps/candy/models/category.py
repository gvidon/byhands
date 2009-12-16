# -*- coding: utf-8 -*-
from django.db import models

#ВЛОЖЕННЫЕ КАТГЕОРИИ
class Category(models.Model):
	parent      = models.ForeignKey('self', verbose_name=u'Родительская категория', blank=True, null=True, related_name='children')
	
	slug        = models.CharField(u'Имя ссылки', help_text='латиница, цифры и "-"', max_length=64)
	title       = models.CharField(u'Название', max_length=64)
	description = models.CharField(u'Краткое описание', max_length=128)
	
	#СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title
	
	#META
	class Meta:
		app_label           = 'candy'
		db_table            = 'category'
		verbose_name        = u'Категория продуктов'
		verbose_name_plural = u'Категории продуктов'
