from django.db import models

class Meta(models.Model):
	url         = models.CharField(u'URL', max_length=255, db_index=True)
	description = models.TextField(u'Meta-Description', max_length=1024)
	keywords    = models.TextField(u'Meta-Keywords', max_length=1024)
	
	def __unicode__(self):
		return self.url
