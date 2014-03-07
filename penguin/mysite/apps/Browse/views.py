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
	username = request.session['username']
	user_ac = User.get_user_by_username(username).area_code
	context = { 'tool_list': Tool.get_tool_by_area_code(user_ac),
		'user_ac': user_ac,
	}
	html = render(request, 'browse.html', context)
	return HttpResponse(html)
