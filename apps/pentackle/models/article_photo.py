# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db                  import models

from article                    import Article
from utils                      import images

class ArticlePhoto(models.Model):
	article = models.ForeignKey(Article, related_name='photos')
	photo   = models.ImageField(upload_to='upload/photos')
	
	#СОХРАНИТЬ ФОТО И СОЗДАТЬ THUMB
	def save(self):
		super(ArticlePhoto, self).save()
		
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
		app_label           = u'pentackle'
		db_table            = 'article_photo'
		verbose_name        = u'Фото для статьи'
		verbose_name_plural = u'Фотографии статьи'
