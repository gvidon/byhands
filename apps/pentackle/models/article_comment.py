# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db                  import models

class ArticleComment(models.Model):
	pub_date = models.DateTimeField(auto_now_add=True)
	user     = models.ForeignKey(User)
	text     = models.TextField()
	
	#СТРОКВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.text
	
	#META
	class Meta:
		app_label           = u'pentackle'
		ordering            = ['pub_date',]
		db_table            = 'article_comment'
		verbose_name        = u'Комментарий'
		verbose_name_plural = u'Комментарии'
