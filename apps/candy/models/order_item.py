# -*- coding: utf-8 -*-
from django.db import models

#ПОЗИЦИИ ЗАКАЗА
class OrderItem(models.Model):
	order    = models.ForeignKey('Order', verbose_name=u'Заказ', related_name='items')
	product  = models.ForeignKey('Product', verbose_name=u'Товар из магазина')
	
	title    = models.CharField(u'Название', max_length=64)
	
	quantity = models.IntegerField(u'Количество', default=1)
	comment  = models.CharField(u'Комментарий заказчика', max_length=128, blank=True, null=True)
	
	price    = models.FloatField(u'Цена')
	sum      = models.FloatField(u'Общая сумма за позицию')
	
	#СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title
	
	#КАТЕГОРИИ ПРОДУКТА ПУНКТА ЗАКАЗА
	def category(self):
		return self.product.category
	
	#SLUG ПРОДУКТА ПУНКТА ЗАКАЗА
	def slug(self):
		return self.product.slug
	
	#META
	class Meta:
		app_label           = 'candy'
		db_table            = 'order_item'
		verbose_name        = u'Позиция'
		verbose_name_plural = u'Позиции заказа'
