from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
	url(r'^register/?'                        , 'register.form'  , name='register'),
	url(r'^activate/(?P<code>[0-9a-zA-Z]+)/?$', 'activate.by_url', name='activate'),
	url(r'^recover/?$'                        , 'recover.form'   , name='recover'),
	url(r'^recover/(?P<code>[0-9a-zA-Z]+)/?$' , 'recover.confirm', name='recover-confirm'),
	url(r'^profile/?$'                        , 'profile.form'   , name='profile'),
	url(r'^user/(?P<username>[\w\d\-_\.]+)/?' , 'public.profile' , name='public-profile'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^logout/?$', 'logout_then_login', name='logout'),
	url(r'^login/?$' , 'login', { 'template_name': 'accounts/login.html' }, name='login'),
)
