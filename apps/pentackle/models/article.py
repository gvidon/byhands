# -*- coding: utf-8 -*-
from datetime                   import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers   import reverse
from django.conf                import settings
from django.db                  import models

from article_comment            import ArticleComment
from tags.models                import Tag
from section                    import Section

class Article(models.Model):
	pub_date  = models.DateTimeField('Publish date', default=datetime.now)
	title     = models.CharField(max_length=200)
	slug      = models.SlugField(help_text='A "Slug" is a unique URL-friendly title for an object.')
	summary   = models.TextField(help_text="A single paragraph summary or preview of the article.")
	body      = models.TextField('Body text')
	
	author    = models.CharField(max_length=255, blank=True, null=True)
	source    = models.CharField(max_length=128, blank=True, null=True)
	
	comments  = models.ManyToManyField(ArticleComment, blank=True)
	tags      = models.ManyToManyField(Tag, related_name='articles', db_table='article_tag', blank=True)
	
	publish   = models.BooleanField(
		u'Опубликовать статью',
		default   = True,
		help_text = u'Статья не появится на сайте пока н опубликована'
	)
	
	sections  = models.ManyToManyField(Section, related_name='articles', blank=True, null=True)
	
	# Custom article manager
	# objects = ArticleManager()
	
	#СТРОКВОЕ ПРЕДСТАВЛЕНИЕ
	def __unicode__(self):
		return self.title
		
	#ПРИКРЕПЛЕНИЕ ТЭГА К СТАТЬЕ
	def attach_tags(self, tags_string):
		for tag in filter(lambda t: t.strip(), set(tags_string.split(','))):
			try:
				self.tags.add(Tag.objects.get(title=tag.strip()))
			
			except Tag.DoesNotExist:
				self.tags.create(title=tag.strip())
	
	#ССЫЛКА НА СТАТЬЮ
	def get_absolute_url(self):
		args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
		return reverse('article-detail', args=args)
	
	#ССЫЛКА НА ТУМБ
	def thumb_url(self):
		try:
			return self.photos.all()[0].thumb_url()
		
		except IndexError:
			return None
	
	class Meta:
		app_label           = 'pentackle'
		db_table            = 'article'
		ordering            = ['-pub_date']
		get_latest_by       = 'pub_date'
		verbose_name        = u'Статья'
		verbose_name_plural = u'Статьи'
