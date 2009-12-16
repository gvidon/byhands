# -*- coding: utf-8 -*-
from django.db                    import models
from django.contrib.auth.models   import User

#ПРОДУКТ С ЦЕНОЙ ОПИСАНИЕМ И ГАБАРИТАМИ
class Product(models.Model):
	author      = models.ForeignKey(User, verbose_name=u'Автор изделия', blank=True, null=True)
	category    = models.ManyToManyField('Category', verbose_name=u'Категория', db_table='category_product_ref', related_name='products')
	
	created_at  = models.DateTimeField(auto_now_add=True)
	
	is_active   = models.BooleanField(u'Показывать в магазине', default=True)
	is_featured = models.BooleanField(u'Рекомендуемый товар', default=False)
	
	slug        = models.CharField(u'Имя ссылки для продукта', help_text='латиница, цифры и "-"', max_length=64)
	title       = models.CharField(u'Название', max_length=64)
	description = models.TextField(u'Описание', blank=True, null=True)
	
	size        = models.CharField(u'Размеры', help_text='в произвольной форме', max_length=64, blank=True, null=True)
	madeof      = models.CharField(u'Материал', max_length=64, blank=True, null=True)
	price       = models.FloatField(u'Цена')
	
	#ССЫЛКА НА ТУМБ
	def thumb_url(self):
		try:
			return self.photos.all()[0].thumb_url()
		
		except IndexError:
			return None
		
	#СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title
	
	#META
	class Meta:
		app_label           = 'candy'
		db_table            = 'product'
		verbose_name        = u'Продукт магазина'
		verbose_name_plural = u'Продукты'
