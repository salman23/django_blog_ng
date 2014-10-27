from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from settings import BASE_DIR

def home(request):
	context = RequestContext(request)
	return render_to_response('project_home.html', context)