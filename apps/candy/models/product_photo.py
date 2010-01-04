# -*- coding: utf-8 -*-
from django.db  import models
from apps.utils import images

#ФОТОГРАФИИ ПРОДУКТА
class ProductPhoto(models.Model):
	product = models.ForeignKey('Product', related_name='photos')
	photo   = models.ImageField(upload_to='upload/products')
	
	#СОХРАНИТЬ ФОТО И СОЗДАТЬ THUMB
	def save(self):
		super(ProductPhoto, self).save()
		
		images.resize(self.photo.path)
		images.generate_thumb(self.photo.path, (150, 150))
	
	#ССЫЛКА НА ТУМБ
	def thumb_url(self):
		return self.photo.url+'_thumb'
	
	#СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.photo.path
	
	#META
	class Meta:
		app_label           = 'candy'
		db_table            = 'product_photo'
		verbose_name        = u'Фото продукта'
		verbose_name_plural = u'Фотографии продукта'
