from django.contrib import admin
from django.conf    import settings
from models         import *

class PhotoInline(admin.TabularInline):
	model   = ProductPhoto
	fk_name = 'product'

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'priority')
	
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'is_paid', 'is_delivered', 'sum')
	
class OrderItemAdmin(admin.ModelAdmin):
	pass

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'price', 'is_active', 'is_featured')
	inlines = [ PhotoInline, ]
	
	def queryset(self, request):
		return Product.mixed.all()
		
	class Media:
		js = (
			settings.MEDIA_URL+'js/lib/jquery.min.js',
			
			'/tinymce/tiny_mce.js',
			settings.MEDIA_URL+'filebrowser/js/TinyMCEAdmin.js',
			
			settings.MEDIA_URL+'js/jqModal.js',
			settings.MEDIA_URL+'js/jquery.timers.js',
		)
		
		css = {'all': (
			settings.MEDIA_URL+'css/jqModal.css',
			settings.MEDIA_URL+'css/crossposting.css',
			
			settings.MEDIA_URL+'js/tinymce/themes/simple/skins/default/ui.css',
			settings.MEDIA_URL+'js/tinymce/themes/advanced/skins/default/ui.css',
			settings.MEDIA_URL+'js/tinymce/themes/advanced/skins/o2k7/ui.css',
		)}

admin.site.register(Category , CategoryAdmin)
admin.site.register(Order    , OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product  , ProductAdmin)

