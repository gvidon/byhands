from django.contrib import admin
from django.conf    import settings
from models         import Meta

class SeoMetaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Meta , SeoMetaAdmin)

