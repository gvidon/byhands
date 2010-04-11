# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template  import RequestContext
from django.conf      import settings

def error_handler(request):
	return render_to_response('500.html', {'media_url': settings.MEDIA_URL})

