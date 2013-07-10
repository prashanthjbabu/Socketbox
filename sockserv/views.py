from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib, urllib2
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

@csrf_exempt
def features(request):
	return render_to_response('features.html', context_instance=RequestContext(request))

@csrf_exempt
def tutorials(request):
	return render_to_response('tutorials.html', context_instance=RequestContext(request))

@csrf_exempt
def contact(request):
	return render_to_response('contact.html', context_instance=RequestContext(request))

@csrf_exempt
def about(request):
	return render_to_response('about.html', context_instance=RequestContext(request))

@csrf_exempt
def js(request):
	return render_to_response('js/socketbox.js', context_instance=RequestContext(request))
