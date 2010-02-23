from django.contrib   import admin
from pentackle.models import ArticleComment, ArticlePhoto, Article, Section

class PhotoInline(admin.TabularInline):
	model   = ArticlePhoto
	fk_name = 'article'

class ArticleCommentAdmin(admin.ModelAdmin):
	pass
	
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')
	inlines = [ PhotoInline, ]
	
class SectionAdmin(admin.ModelAdmin):
	pass

admin.site.register(ArticleComment, ArticleCommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)

