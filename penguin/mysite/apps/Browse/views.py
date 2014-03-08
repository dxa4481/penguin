from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..Tools.models import User, Tool

# Create your views here.

def browse_tools(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	area_code = request.session['area_code']
	tools =  Tool.get_tool_by_area_code(area_code)
	context = { 'tool_list': tools,
		'user_ac': area_code,
	}
	html = render(request, 'browse.html', context)
	return HttpResponse(html)
