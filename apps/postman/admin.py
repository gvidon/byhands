from django.contrib import admin
from django.conf    import settings
from models         import *

class SubscriberAdmin(admin.ModelAdmin):
	pass
	
class MailAdmin(admin.ModelAdmin):
	pass
	
class SentLogAdmin(admin.ModelAdmin):
	pass

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(SentLog   , SentLogAdmin)
admin.site.register(Mail      , MailAdmin)
