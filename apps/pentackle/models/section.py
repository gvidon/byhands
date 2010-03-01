# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db                import models

class Section(models.Model):
	title = models.CharField(max_length=80, unique=True)
	slug  = models.SlugField()
	
	#СТРОКВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('pr-section', args=[self.slug])

	class Meta:
		app_label           = u'pentackle'
		db_table            = 'article_section'
		ordering            = ['title']
		verbose_name        = u'Раздел'
		verbose_name_plural = u'Разделы'
