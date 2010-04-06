# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template  import RequestContext

def error_handler(request):
	return render_to_response('500.html', context_instance=RequestContext(request))
