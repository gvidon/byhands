# -*- coding: utf-8 -*-
from datetime                       import datetime

from django.template.context        import RequestContext
from django.shortcuts               import render_to_response
from django.shortcuts               import get_object_or_404
from django.http                    import HttpResponse, Http404

def process(request):
	if not request.GET.get('query'):
		return render_to_response('search/form.html', context_instance=RequestContext(request))
