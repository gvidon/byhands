# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db                  import models

# Описание ЗАКАЗА
class Order(models.Model):
	user         = models.ForeignKey(User, verbose_name=u'Аккаунт пользователя')
	created_at   = models.DateTimeField(auto_now_add=True)
	
	name         = models.CharField(u'Имя заказчика', max_length=64, blank=True, null=True)
	email        = models.EmailField(max_length=128)
	phone        = models.CharField(u'Телефон', max_length=16)
	city         = models.CharField(u'Город', max_length=32)
	address      = models.CharField(u'Адрес', max_length=255)
	
	is_confirmed = models.BooleanField(u'Подтвержден пользователем', default=False)
	is_cancelled = models.BooleanField(u'Отменен', default=False)
	is_paid      = models.BooleanField(u'Оплачен', default=False)
	is_delivered = models.BooleanField(u'Доставлен', default=False)
	
	sum          = models.FloatField(u'Общая сумма заказа')
	
	delivery_by = models.CharField(u'Способ доставки', choices=(
		('post', u'Почта России'),
		('ems' , u'EMS'),
		('pek' , u'ПЭК'),
	), max_length=4)
	
	payment_type = models.CharField(u'Способ оплаты', max_length=32, choices=(
		(u'Наличные'     , 'cash'),
		(u'WebMoney'     , 'webmoney'),
		(u'Яндекс.деньги', 'yandex'),
	))
	
	# СТРОКОВОЕ представление
	def __unicode__(self):
		return str(self.id)
	
	# META
	class Meta:
		app_label           = 'candy'
		db_table            = 'order'
		verbose_name        = u'Заказ'
		verbose_name_plural = u'Заказы'
