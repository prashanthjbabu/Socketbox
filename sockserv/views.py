from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib, urllib2
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))